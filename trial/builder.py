import base64
import io
import re
from pathlib import Path

import itables
import polars as pl
import seaborn as sns


class Builder:
    """"""

    def __init__(self):
        """"""
        f_data = Path(__file__).parent.resolve() / "data"

        print("load datasets:")

        name = "iris"
        print(name)
        p_data = f_data / f"{name}.csv"
        self.df_iris = pl.read_csv(p_data)

        name = "penguins"
        print(name)
        p_data = f_data / f"{name}.csv"
        self.df_penguins = pl.read_csv(p_data)

        name = "tips"
        print(name)
        p_data = f_data / f"{name}.csv"
        self.df_tips = pl.read_csv(p_data)

        name = "fmri"
        print(name)
        p_data = f_data / f"{name}.csv"
        self.df_fmri = pl.read_csv(p_data)

        name = "countries"
        print(name)
        p_data = f_data / f"{name}.csv"
        self.df_countries = pl.read_csv(p_data)

        # print()
        # print("load iptables datasets:")

        # name = "countries"
        # print(name)
        # self.df_countries = itables.sample_dfs.get_countries(html=False)

        self.f_out = Path("output")
        self.f_out.mkdir(exist_ok=True)

    def init_jupyter_iptables(self):
        """"""
        itables.init_notebook_mode()

        itables.options.layout = {
            "topStart": "pageLength",
            "topEnd": "search",
            "bottomStart": "info",
            "bottomEnd": "paging",
        }

        print("dataframes display in interactive mode in this notebook")

    def build_plot_penguins(self):
        """"""
        sns.set_theme(context="notebook")

        g = sns.lmplot(
            data=self.df_penguins,
            x="bill_length_mm",
            y="bill_depth_mm",
            hue="species",
            height=5,
            aspect=8 / 5,
        )
        g.set_axis_labels("Snoot length (mm)", "Snoot depth (mm)")

        name = "penguins"
        img_fmt = "png"

        self.save(g, name, img_fmt)

    def build_plot_tips(self):
        """"""
        sns.set_theme(context="notebook", style="darkgrid")

        g = sns.jointplot(
            x="total_bill",
            y="tip",
            data=self.df_tips,
            kind="reg",
            truncate=False,
            xlim=(0, 60),
            ylim=(0, 12),
            color="m",
            height=5,
        )
        g.set_axis_labels("Total Bill", "Tip (USD)")

        name = "tips"
        img_fmt = "png"

        self.save(g, name, img_fmt)

    def build_plot_fmri(self):
        """"""
        sns.set_theme(context="notebook", style=None)

        g = sns.relplot(
            data=self.df_fmri,
            kind="line",
            x="timepoint",
            y="signal",
            hue="event",
        )

        name = "fmri"
        img_fmt = "png"

        self.save(g, name, img_fmt)

    def save(
        self,
        g: sns.JointGrid,
        name: str,
        img_fmt="png",
        transparent=False,
    ):
        """"""
        p_out = self.f_out / f"{name}.{img_fmt}"
        print(f"save {name} to {p_out}")
        g.savefig(p_out, format=img_fmt, transparent=transparent)

        print(f"save {name} to io")
        f = io.BytesIO()
        g.figure.savefig(f, format=img_fmt, transparent=transparent)
        f.seek(0)
        img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode("ascii")

        p_out = self.f_out / f"{name}.b64.txt"
        print(f"save {name} to {p_out}")
        p_out.write_text(img_b64)

        p_out = self.f_out / f"{name}.img-tag.txt"
        img_tag = self.build_img_tag(img_b64, img_fmt=img_fmt)
        p_out.write_text(img_tag)

    def build_img_tag(self, b64: str, img_fmt="png"):
        """"""
        tpl = """<img src="data:image/__img_fmt__;base64, __b64__">"""

        out = tpl
        out = re.sub("__img_fmt__", img_fmt, out)
        out = re.sub("__b64__", b64, out)

        return out


# --- mail

# msg.add_header('Content-Type','text/html')
# msg.set_content(f'''<html>
# <head></head>
# <body>
# <img src="data:image/{img_format};base64, {b64encode(img_data).decode('ascii')}">
# </body>
# </html>''')

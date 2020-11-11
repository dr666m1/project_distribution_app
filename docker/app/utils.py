import contextlib
import scipy.stats
import pandas as pd
import numpy as np
import altair as alt
from altair import expr, datum
import streamlit as st

class ApplicationError(Exception):
    """exceptions raised by this application"""


class Config:
    is_continuous = True
    is_pdf = True


@contextlib.contextmanager
def using_config(config_dict):
    old_value = {}
    for k, v in config_dict.items():
        old_value[k] = getattr(Config, k)
        setattr(Config, k, v)
    try:
        yield
    finally:
        for k, v in old_value.items():
            setattr(Config, k, v)


def is_distribution(x):
    parent = scipy.stats.rv_continuous if Config.is_continuous else scipy.stats.rv_discrete
    try:
        return issubclass(type(x), parent)
    except TypeError as e:
        return False


class DFGenerator:
    def __init__(self, distribution, label, x_min, x_max, args):
        self.distribution = distribution
        self.label = label
        self.x_min = x_min
        self.x_max = x_max
        self.args = args

    def _pdf_or_pmf(self):
        if Config.is_continuous:
            return self.distribution.pdf
        else:
            return self.distribution.pmf

    def _generate_x(self):
        if Config.is_continuous:
            return np.linspace(self.x_min, self.x_max, 1000)
        else:
            return np.arange(int(self.x_min), int(self.x_max)+1)

    def _generate_y(self, x_value):
        method = self._pdf_or_pmf() if Config.is_pdf else self.distribution.cdf
        return [method(*a) for a in [[x]+self.args for x in x_value]]

    def generate_df(self):
        x_value = self._generate_x()
        y_value = self._generate_y(x_value)
        df = pd.DataFrame({"label": self.label, "x": x_value, "y": y_value})
        df["y"].replace([np.inf, -np.inf, 0], np.nan, inplace=True)
        ret = df.dropna()
        if ret.shape[0] == 0:
            raise ApplicationError
        return ret


def generate_chart(df):
    if Config.is_continuous:
        line = alt.Chart(df).mark_line().encode(
            x="x",
            y="y",
            color="label"
        )
        nearest = alt.selection(
            type="single",
            nearest=True,
            on="mouseover",
            encodings=["x"],
            empty="none",
        )
        selectors = alt.Chart(df).mark_point().encode(
            x='x',
            opacity=alt.value(0),
        ).add_selection(nearest)
        rules = alt.Chart(df).mark_rule(color='gray').encode(
            x='x',
        ).transform_filter(nearest)
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )
        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'y_:Q', alt.value(' '))
        ).transform_calculate(y_=expr.round(datum.y*100)/100)
        chart = alt.layer(line, selectors, rules, points, text)
    else:
        chart = alt.Chart(df).mark_bar(opacity=0.6).encode(
            x="x:O",
            y=alt.Y('y', stack=None),
            color="label",
        ).interactive()
    return chart


help_message = f"""
    ### usage
    choose probability distributions to plot and pass arguments.  
    you can read the docstring to check valid arguments.  
    ### example
    according to the docstring, you can pass three arguments to
    *scipy.stats.norm.pdf()*.  
    since `x`(or `k`) is automatically passed,
    you can pass other arguments `loc`, `scale`.  
    if you want to plot *N(0, 1^2)*,
    fill `args n` with `0,1` (or leave it blank to use default value).
    ```
    Method
    ---
    pdf(x, loc=0, scale=1)
        Probability density function.)
    cdf(x, loc=0, scale=1)
        Cumulative distribution function.)
    ```
"""

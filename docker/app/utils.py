import contextlib
import scipy.stats
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

def is_distribution(x):
    parent = scipy.stats.rv_continuous if Config.is_continuous else scipy.stats.rv_discrete
    try:
        return issubclass(type(x), parent)
    except TypeError as e:
        return False

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


def generate_df(distribution, args, label, x_min=-3, x_max=3):
    x_value = _generate_x(x_min, x_max)
    y_value = _generate_y(distribution, x_value, args)
    df = pd.DataFrame({
        "label": label,
        "x": x_value,
        "y": y_value,
    })
    df["y"].replace([np.inf, -np.inf, 0], np.nan, inplace=True)
    return df.dropna()

def _generate_x(x_min, x_max):
    if Config.is_continuous:
        return np.linspace(x_min, x_max, 1000)
    else:
        return np.arange(int(x_min), int(x_max)+1)

def _generate_y(distribution, x_value, args):
    try:
        method = distribution.pdf if Config.is_pdf else distribution.cdf
    except AttributeError as e:
        method = distribution.pmf
    return [method(*a) for a in [[x]+args for x in x_value]]

def plot_chart(df):
    if Config.is_continuous:
        chart = alt.Chart(df).mark_line().encode(
            x="x",
            y="y",
            color="label"
        ).interactive()
    else:
        chart = alt.Chart(df).mark_bar(opacity=0.6).encode(
            x="x:O",
            y=alt.Y('y', stack=None),
            color="label",
        ).interactive()
    st.altair_chart(chart, use_container_width=True)


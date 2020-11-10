import streamlit as st
import numpy as np
import pandas as pd
import scipy.stats as stats
import inspect
import altair as alt
import utils

st.markdown("""# Distribution Sandbox""")
n_choice = 2

# sidebar
method = st.sidebar.selectbox("method", [
    "pdf (probability density function)",
    "cdf (cumulative density function)",
])
x_min = st.sidebar.number_input("x_min", value=-3.0, step=0.5)
x_max = st.sidebar.number_input("x_max", value=+3.0, step=0.5)
distributions = {x[0]: x[1] for x in inspect.getmembers(stats, utils.is_continuous)}

choices = []
args = []
for i in range(n_choice):
    choices.append(st.sidebar.selectbox(
        f"probability distribution {i}",
        [None] + list(distributions.keys())
    ))
    arg_text  = st.sidebar.text_area(f"args {i}")
    args.append([float(x) for x in arg_text.split(",")] if arg_text else [])


# graph
if not any(choices):
    st.markdown("""
        ### usage
        choose probability distributions to plot and pass arguments.  
        you can read the docstring to check valid arguments.  
        ### example
        according to the docstring, you can pass three arguments to
        *scipy.stats.norm.pdf()*.  
        since `x` is automatically passed,
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
    """)
st.markdown(f"""## graph""")
dfs = []

for i in range(n_choice):
    if choices[i]:
        x_value = np.linspace(x_min, x_max, 1000)
        try:
            if method == "pdf (probability density function)":
                y_value = [distributions[choices[i]].pdf(*a) for a in [[x]+args[i] for x in x_value]]
            else:
                y_value = [distributions[choices[i]].cdf(*a) for a in [[x]+args[i] for x in x_value]]

            dfs.append(pd.DataFrame({
                "choice": f"{i}: {choices[i]}",
                "x": x_value,
                "y": y_value,
            }))
        except TypeError as e:
            st.markdown(f"""
                maybe you passed invalid args as `args {i}`!  
                see the docstring below and check the args of {method}.
            """)
            break

if dfs:
    df = pd.concat(dfs, ignore_index=True).replace([np.inf, -np.inf, 0], np.nan).dropna()
    chart = alt.Chart(df).mark_line().encode(
        x="x",
        y="y",
        color="choice"
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

# doc
st.markdown(f"""## docstrings""")
for c in set(choices):
    if c is not None:
        with st.beta_expander(f"docstring of {c}"):
            st.write(distributions[c].__doc__)
issubclass(type(stats.multivariate_normal), stats.rv_continuous)

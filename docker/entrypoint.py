import streamlit as st
import numpy as np
import pandas as pd
import scipy.stats as stats
import inspect
import altair as alt
import app

st.markdown("""# Distribution Sandbox""")
n_choice = 2

# sidebar
c_or_d = st.sidebar.selectbox("continuous or discrete", ["continuous","discrete",])
is_continuous = True if c_or_d == "continuous" else False

method = st.sidebar.selectbox("method", ["pdf (or pmf)", "cdf",])
is_pdf = True if method == "pdf (or pmf)" else False

x_min = st.sidebar.number_input("x_min", value=-10.0, step=1.0)
x_max = st.sidebar.number_input("x_max", value= 10.0, step=1.0)

with app.using_config({"is_continuous": is_continuous}):
    distributions = {x[0]: x[1] for x in inspect.getmembers(stats, app.is_distribution)}

choices = []
args = []
for i in range(n_choice):
    choices.append(st.sidebar.selectbox(
        f"probability distribution {i}",
        [None] + list(distributions.keys())
    ))
    arg_text  = st.sidebar.text_area(f"args {i}")
    args.append([float(x) for x in arg_text.split(",")] if arg_text else [])


# help
with st.beta_expander(f"need some help?"):
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

# graph
st.markdown(f"""## graph""")
dfs = []

if not any(choices):
    st.markdown(f"""**no probability distribution is selected!!**""")

with app.using_config({"is_continuous": is_continuous, "is_pdf": is_pdf}):
    for i in range(n_choice):
        if not choices[i]:
            break
        try:
            dfs.append(app.generate_df(
                distributions[choices[i]],
                args[i],
                f"{i}: "+choices[i],
                x_min,
                x_max,
            ))
        except TypeError as e:
            st.markdown(f"""
                maybe you passed invalid args as `args {i}`!  
                see the docstring below and check the args of {method}.
            """)
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        app.plot_chart(df)

# doc
st.markdown(f"""## docstrings""")
if not any(choices):
    st.markdown(f"""**no probability distribution is selected!!**""")

for c in set(choices):
    if c:
        with st.beta_expander(f"docstring of {c}"):
            st.write(distributions[c].__doc__)

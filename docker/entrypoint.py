import app
import inspect
import os
import pandas as pd
import scipy.stats
import streamlit as st

st.markdown("""# Probability Distribution Sandbox""")
n_choice = int(os.environ.get("N_CHOICE", 1))

##### sidebar #####
c_or_d = st.sidebar.selectbox("continuous or discrete", ["continuous","discrete",])
is_continuous = True if c_or_d == "continuous" else False

method = st.sidebar.selectbox("method", ["pdf (or pmf)", "cdf",])
is_pdf = True if method == "pdf (or pmf)" else False

x_min = st.sidebar.number_input("x_min", value=-10, step=1)
x_max = st.sidebar.number_input("x_max", value= 10, step=1, min_value=x_min)

with app.using_config({"is_continuous": is_continuous}):
    distributions = {x[0]: x[1] for x in inspect.getmembers(scipy.stats, app.is_distribution)}

choices = []
args = []
for i in range(n_choice):
    choices.append(st.sidebar.selectbox(
        f"probability distribution {i}",
        [None] + list(distributions.keys())
    ))
    arg_text  = st.sidebar.text_input(f"args {i}")
    args.append([float(x) for x in arg_text.split(",")] if arg_text else [])


##### help #####
with st.beta_expander(f"need some help?"):
    st.markdown(app.help_message)

##### graph #####
st.markdown(f"""## graph""")
dfs = []

if not any(choices):
    st.markdown(f"""**no probability distribution is selected!!**""")

with app.using_config({"is_continuous": is_continuous, "is_pdf": is_pdf}):
    for i in range(n_choice):
        if not choices[i]:
            continue
        df_gen = app.DFGenerator(
            distribution=distributions[choices[i]],
            label=f"{i}: {choices[i]}",
            x_min=x_min,
            x_max=x_max,
            args=args[i],
        )
        try:
            dfs.append(df_gen.generate_df())
        except TypeError as e:
            st.markdown(f"""
                maybe you passed invalid args as `args {i}`!  
                see the docstring below and check the args of {method}.
            """)
        except app.ApplicationError as e:
            st.markdown(f"""
                empty data was generated.  
                please check `x_min`, `x_max` and `args {i}`.  
                the docstrings below might be helpful.
            """)

    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        chart = app.generate_chart(df)
        st.altair_chart(chart, use_container_width=True)

##### docstring #####
st.markdown(f"""## docstrings""")
if not any(choices):
    st.markdown(f"""**no probability distribution is selected!!**""")

for c in set(choices):
    if not c: # ignore None
        continue
    with st.beta_expander(f"docstring of {c}"):
        st.write(distributions[c].__doc__)


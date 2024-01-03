import streamlit as st
import pandas as pd
import plotly.express as px
from cache_func import get_medals

st.set_page_config(layout="wide")

st.header("Medal Analysis")

df_athlete_medals = get_medals()
st.dataframe(df_athlete_medals.style.format({"Year": lambda x: "{:}".format(x)}))

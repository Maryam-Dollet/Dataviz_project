import streamlit as st
import pandas as pd
import plotly.express as px
from cache_func import get_medals

st.header("Medal Analysis")

df_athlete_medals = get_medals()
st.dataframe(df_athlete_medals)

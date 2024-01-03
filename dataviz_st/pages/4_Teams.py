import streamlit as st
import pandas as pd
import plotly.express as px
from cache_func import get_regions

st.header("Team Analysis")

df_regions = get_regions()

fig = px.choropleth(
    df_regions,
    locations="region",
    color="count",
    hover_name="region",
    animation_frame="Year",
    title="Countries per Year",
    color_continuous_scale="Viridis",
    locationmode="country names",
)

st.plotly_chart(fig)

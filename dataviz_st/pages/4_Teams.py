import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from cache_func import get_regions

st.header("Team Analysis")

season = option_menu("Choose Season", ["Summer", "Winter"], orientation="horizontal")
df_regions = get_regions(season)

fig = px.choropleth(
    df_regions,
    locations="region",
    color="count",
    hover_name="region",
    animation_frame="Year",
    title=f"Participating Countries of the {season} Games Each Years",
    color_continuous_scale="Viridis",
    locationmode="country names",
    width=1200,
    height=800,
)

st.plotly_chart(fig)

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from cache_func import get_regions, get_city_position

st.set_page_config(layout="wide")

st.header("Team Analysis")
with st.sidebar:
    season = option_menu("Choose Season", ["Summer", "Winter"])

df_regions = get_regions(season)
df_city_positions = get_city_position(season)

fig = px.choropleth(
    df_regions,
    locations="region",
    color="participants number",
    hover_name="region",
    animation_frame="Year",
    title=f"Participating Countries of the {season} Games Each Year",
    color_continuous_scale="Viridis",
    locationmode="country names",
    width=1200,
    height=800,
)

st.plotly_chart(fig)

fig = px.line(
    df_regions,
    x="Year",
    y="participants number",
    color="region",
    title=f"Number of athletes per year and per country for {season} Games",
    width=1450,
    height=800,
)
fig.update_xaxes(type="category")
st.plotly_chart(fig)

fig = px.scatter_geo(
    df_city_positions,
    lat=df_city_positions.latitude,
    lon=df_city_positions.longitude,
    hover_name="description",
)
fig.update_layout(width=1300, height=1000, title=f"Host Cities of {season} Games")
st.plotly_chart(fig)

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from cache_func import get_regions, get_city_position

st.header("Team Analysis")

season = option_menu("Choose Season", ["Summer", "Winter"], orientation="horizontal")
df_regions = get_regions(season)
df_city_positions = get_city_position(season)
st.dataframe(df_city_positions)

fig = px.choropleth(
    df_regions,
    locations="region",
    color="participants number",
    hover_name="region",
    animation_frame="Year",
    title=f"Participating Countries of the {season} Games Each Years",
    color_continuous_scale="Viridis",
    locationmode="country names",
    width=1200,
    height=800,
)

st.plotly_chart(fig)


# fig = go.Figure(
#     data=go.Scattergeo(
#         lon=df_city_positions["longitude"],
#         lat=df_city_positions["latitude"],
#         text=df_city_positions["description"],
#         mode="markers",
#     )
# )

fig = px.scatter_geo(
    df_city_positions,
    lat=df_city_positions.latitude,
    lon=df_city_positions.longitude,
    hover_name="description",
)
fig.update_layout(width=1000, height=800)
st.plotly_chart(fig)

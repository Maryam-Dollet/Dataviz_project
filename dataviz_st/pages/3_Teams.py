import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from cache_func import get_regions, get_city_position, filter_df

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
    color_continuous_scale="Purp",
    locationmode="country names",
    width=1200,
    height=800,
)

st.plotly_chart(fig)

# st.dataframe(df_regions.style.format({"Year": lambda x: "{:}".format(x)}))

fig = px.line(
    df_regions,
    x="Year",
    y="participants number",
    color="region",
    title=f"Number of athletes per year and per country for {season} Games",
    width=1450,
    height=800,
)
# fig.update_xaxes(type="category")
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig)

top_10_countries = (
    df_regions.groupby("region")["participants number"]
    .sum()
    .reset_index()
    .sort_values("participants number", ascending=False)
    .head(10)
)
# st.dataframe(top_10_countries)

fig = px.bar(
    top_10_countries,
    x="region",
    y="participants number",
    color="region",
    title="Top 10 countries with the most athletes",
    width=1000,
    height=600,
)
st.plotly_chart(fig)

top_10_countries_per_year = (
    df_regions.groupby("Year")
    .apply(lambda x: x.nlargest(10, ["participants number"]))
    .reset_index(drop=True)
)
# st.dataframe(top_10_countries_per_year)

st.subheader("Number of Athletes over the Years")
year = st.select_slider(
    "Select the Year", options=top_10_countries_per_year.Year.unique()
)
top_10_countries_per_year_filtered = filter_df(top_10_countries_per_year, year)

fig = px.bar(
    top_10_countries_per_year_filtered,
    x="region",
    y="participants number",
    title=f"{season} Game Number of Athletes Evolution of Top 10 Countries over the years",
    color="region",
    width=1400,
    height=700,
)
fig.update_xaxes(tickangle=45)
# fig["layout"].pop("updatemenus")
st.plotly_chart(fig)

fig = px.scatter_geo(
    df_city_positions,
    lat=df_city_positions.latitude,
    lon=df_city_positions.longitude,
    hover_name="description",
)
fig.update_layout(width=1300, height=1000, title=f"Host Cities of {season} Games")
st.plotly_chart(fig)

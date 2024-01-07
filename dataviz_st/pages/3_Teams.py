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

fig = px.choropleth(
    df_regions,
    locations="region",
    color="participants number",
    hover_name="region",
    animation_frame="Year",
    title=f"Participating Countries of the {season} Games Each Year",
    color_continuous_scale="Purp",
    locationmode="country names",
    width=1000,
    height=800,
)
fig.update_geos(
    lataxis=dict(showgrid=True, gridwidth=0.2, griddash="solid", gridcolor="#000"),
    lonaxis=dict(showgrid=True, gridwidth=0.2, griddash="solid", gridcolor="#000"),
    showcountries=True,
    countrycolor="#999",
)

st.plotly_chart(fig)

st.write(
    "The graph represents the evolution of the number of participant of each country in the olympic games. We can see that the number of participants in each countrie's team has been increasing since the creation of the olympic games. However each countries' number of participants can vary a lot from one year to another. This can be explained by the degree of interest of the country in the olympic games. "
)

if season == "Winter":
    st.write(
        "Countries where there is a possibility to practive Winter Sport do participate more it the Winter Games. The lack of Southern country participation may be explained by the lack of the favourable environment as well as the low development of the winter sports in some."
    )
else:
    st.write(
        "For example, the number of participants of the United States of America in the summer olympic games of 1980 is very low because the country boycotted the olympic games of 1980."
    )

# st.dataframe(df_regions.style.format({"Year": lambda x: "{:}".format(x)}))

fig = px.line(
    df_regions,
    x="Year",
    y="participants number",
    color="region",
    title=f"Number of athletes per year and per country for {season} Games",
    width=1000,
    height=600,
)
# fig.update_xaxes(type="category")
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig)

st.write(
    "We observe a growth in the number of athletes participating since the creation of the olympic games. This can be explained by the fact that the number of sports has been increasing since the creation of the olympic games and the inclusion of feminine athletes in the olympic games."
)

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
    title=f"Top 10 Countries with the most Athletes {season} Games {year} ",
    color="region",
    width=1000,
    height=600,
)
fig.update_xaxes(tickangle=45)
# fig["layout"].pop("updatemenus")
st.plotly_chart(fig)

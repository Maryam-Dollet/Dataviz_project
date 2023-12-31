import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from cache_func import get_medals, load_datasets

st.set_page_config(layout="wide")

st.header("Medal Analysis")
with st.sidebar:
    season = option_menu("Choose Season", ["Summer", "Winter"])

df_athlete_medals = get_medals(season)
df_merged = load_datasets()
# df_medals_sorted = df_athlete_medals.sort_values(
#     by=["Year", "Gold", "Silver", "Bronze"]
# ).reset_index(drop=True)
# st.dataframe(df_medals.style.format({"Year": lambda x: "{:}".format(x)}))
# st.dataframe(
#     df_athlete_medals.sort_values(by=["Year", "Gold", "Bronze", "Silver"])
#     .reset_index(drop=True)[::-1]
#     .reset_index(drop=True)
#     .style.format({"Year": lambda x: "{:}".format(x)})
# )

# st.dataframe(df_medals[(df_medals["region"] == "USA") & (df_medals["Year"] == 1896)].style.format({"Year": lambda x: "{:}".format(x)}))
# st.dataframe(df_medals[(df_medals["region"] == "Germany") & (df_medals["Year"] == 1896)].style.format({"Year": lambda x: "{:}".format(x)}))

st.subheader(f"Winners of the {season} Games")
year = st.select_slider("Select the Year", options=df_athlete_medals.Year.unique())

df_filtered = (
    df_athlete_medals[df_athlete_medals["Year"] == year]
    .sort_values(by=["Gold", "Silver", "Bronze"], ascending=False)
    .reset_index(drop=True)[["region", "Gold", "Silver", "Bronze", "Total"]]
)

col4, col1, col2, col3, col5 = st.columns(5)

with col1:
    st.metric("2nd Place :second_place_medal:", value=f"{df_filtered.iloc[1].region}")

with col2:
    st.metric("1st Place :first_place_medal:", value=f"{df_filtered.iloc[0].region}")

with col3:
    st.metric("3rd Place :third_place_medal:", value=f"{df_filtered.iloc[2].region}")

col21, col22 = st.columns(2)
city = df_merged[df_merged["Year"] == year].iloc[0].City
df_filtered.insert(0, "Place", df_filtered.index + 1)

with col21:
    st.subheader(f"Leaderboard {city} {year} {season} Games")
    st.dataframe(
        df_filtered.style.format({"Year": lambda x: "{:}".format(x)}),
        hide_index=True,
        width=500,
    )

with col22:
    fig = px.bar(
        df_filtered.head(3),
        x="region",
        y=["Gold", "Silver", "Bronze"],
        barmode="group",
        text_auto=".1s",
        title="Winner Medal Distribution",
        width=600,
    )
    st.plotly_chart(fig)


fig = px.choropleth(
    df_athlete_medals,
    locations="region",
    color="Total",
    hover_name="region",
    animation_frame="Year",
    title=f"{season} Game Total Medals Evolution per Country over the years",
    color_continuous_scale="Purp",
    locationmode="country names",
    width=1000,
    height=800,
)
fig.update_geos(bgcolor="#0E1117", coastlinecolor="#fff")
fig.update_traces(
    marker_line_color="#000", marker_line_width=1.5, selector=dict(type="choropleth")
)
st.plotly_chart(fig)

st.write(
    "This graph allows us to have a representation of the evolution of particular countries regarding their athletic performances in the olympic games. It can somehow reflect the international country's influence and the evolution of the country itself."
)

fig = px.bar(
    df_athlete_medals.sort_values(by=["Year", "Gold", "Silver", "Bronze"]),
    x="region",
    y=["Gold", "Silver", "Bronze"],
    title=f"{season} Game Medal Evolution per Country over the years",
    barmode="group",
    width=1000,
    height=600,
    text_auto=".1s",
    animation_frame="Year",
    # animation_group="medal_count",
)
fig.update_xaxes(tickangle=45)
# fig["layout"].pop("updatemenus")
st.plotly_chart(fig)

st.write(
    "All the graph representing the ranking of the countries by the number of medals won are ranking according to the amount of gold medals won. In case of a tie, the countries are ranked by the number of silver medals won etc."
)

# st.dataframe(df_athlete_medals.groupby("Year").apply(lambda x: x.nlargest(10,['Gold',"Silver", "Bronze"])).reset_index(drop=True))
df_top_10 = (
    df_athlete_medals.groupby("Year")
    .apply(lambda x: x.nlargest(10, ["Gold", "Silver", "Bronze"]))
    .reset_index(drop=True)
)


yrange = [0, 80] if season == "Summer" else [0, 15]

fig = px.bar(
    df_top_10,
    x="region",
    y=["Gold", "Silver", "Bronze"],
    title=f"{season} Game Medal Evolution of Top 10 Countries over the years",
    barmode="group",
    width=1000,
    height=600,
    range_y=yrange,
    text_auto=".1s",
    animation_frame="Year",
    # animation_group="medal_count",
)
fig.update_xaxes(tickangle=45)
# fig["layout"].pop("updatemenus")
st.plotly_chart(fig)

if season == "Summer":
    st.write(
        "We can see that across time, USA and Russia appear to be winners of the Olymic Games more often, the rivalry between those two countries in the 20th century are even reflected in the Olympic Games."
    )
else:
    st.write(
        "As Winter Games are only accessible in the Northern Countries where the temperatures are low and the Winter Sport practice is high, it is not surprising that among the winners Finland, Germany, Norway and Russia appear the most. "
    )

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from cache_func import get_medals

st.set_page_config(layout="wide")

st.header("Medal Analysis")
season = option_menu("Choose Season", ["Summer", "Winter"], orientation="horizontal")

_, df_athlete_medals = get_medals(season)
# df_medals_sorted = df_athlete_medals.sort_values(
#     by=["Year", "Gold", "Silver", "Bronze"]
# ).reset_index(drop=True)
# st.dataframe(df_medals.style.format({"Year": lambda x: "{:}".format(x)}))
st.dataframe(df_athlete_medals.style.format({"Year": lambda x: "{:}".format(x)}))

# st.dataframe(df_medals[(df_medals["region"] == "USA") & (df_medals["Year"] == 1896)].style.format({"Year": lambda x: "{:}".format(x)}))
# st.dataframe(df_medals[(df_medals["region"] == "Germany") & (df_medals["Year"] == 1896)].style.format({"Year": lambda x: "{:}".format(x)}))

fig = px.choropleth(
    df_athlete_medals,
    locations="region",
    color="Total",
    hover_name="region",
    animation_frame="Year",
    title=f"{season} Game Medals per Country",
    color_continuous_scale="Viridis",
    locationmode="country names",
    width=1200,
    height=800,
)

st.plotly_chart(fig)

fig = px.bar(
    df_athlete_medals.sort_values(by=["Year", "Gold", "Silver", "Bronze"]),
    x="region",
    y=["Gold", "Silver", "Bronze"],
    title=f"{season} Game Medals per Country",
    barmode="group",
    width=1400,
    height=800,
    text_auto=".1s",
    animation_frame="Year",
    # animation_group="medal_count",
)
fig.update_xaxes(tickangle=45)
# fig["layout"].pop("updatemenus")
st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from cache_func import get_medals

st.set_page_config(layout="wide")

st.header("Medal Analysis")
with st.sidebar:
    season = option_menu("Choose Season", ["Summer", "Winter"])

df_athlete_medals = get_medals(season)
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

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("2nd Place", value=f"{df_filtered.iloc[1].region}")

with col2:
    st.metric("1st Place", value=f"{df_filtered.iloc[0].region}")
    st.subheader(f"Leaderboard {year}")
    df_filtered.insert(0, "Place", df_filtered.index + 1)
    st.dataframe(
        df_filtered.style.format({"Year": lambda x: "{:}".format(x)}), hide_index=True
    )

with col3:
    st.metric("3rd Place", value=f"{df_filtered.iloc[2].region}")

fig = px.choropleth(
    df_athlete_medals,
    locations="region",
    color="Total",
    hover_name="region",
    animation_frame="Year",
    title=f"{season} Game Total Medals Evolution per Country over the years",
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
    title=f"{season} Game Medals Evolution per Country over the years",
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

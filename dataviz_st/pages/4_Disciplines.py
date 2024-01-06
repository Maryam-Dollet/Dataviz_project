import streamlit as st
import plotly.express as px
import numpy as np
from cache_func import load_datasets
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

with st.sidebar:
    season = option_menu("Choose Season", ["Summer", "Winter"])

st.header("Disciplines")
st.subheader("Distributed Medals")

df_merged = load_datasets()
games = df_merged[df_merged.Season == season]

medals = (
    games.groupby(["Year", "Sport", "Medal"]).size().reset_index(name="Nb of medals")
)
# st.dataframe(medals.head(3))

medals = medals.pivot_table(
    index=["Year", "Sport"], columns="Medal", values="Nb of medals", aggfunc="sum"
).reset_index()
# st.dataframe(medals.head(15))

medals = medals.fillna(0)
medals = medals.astype({"Gold": "int32", "Silver": "int32", "Bronze": "int32"})

medals["Total Nb of Medals distributed"] = (
    medals["Gold"] + medals["Silver"] + medals["Bronze"]
)
# st.dataframe(medals.head(15))

fig = px.bar(
    medals,
    x="Sport",
    y=["Gold", "Silver", "Bronze"],
    title=f"Number of Medals distributed per Sport in {season} Games",
    width=1000,
    height=600,
)
fig.update_layout(barmode="stack", xaxis={"categoryorder": "total descending"})
fig.update_xaxes(tickangle=45)

st.plotly_chart(fig)

st.write(
    "The number of medals distributed per sport varies a lot. This can be explained by the fact that some sports have more events than others. For example, the sport of swimming has 34 events whereas the sport of golf has only 2 events."
)

# st.dataframe(games)

unique_events = games.drop_duplicates(subset=["Year", "Sport", "Event"])[
    ["Year", "Sport", "Event"]
].sort_values("Year", ignore_index=True)

# st.dataframe(unique_events)

conditions = [
    (unique_events["Event"].str.contains("Men")),
    (unique_events["Event"].str.contains("Women")),
    (unique_events["Event"].str.contains("Mixed")),
]

values = ["Men", "Women", "Mixed"]

unique_events["category"] = np.select(conditions, values, default=0)

# st.dataframe(unique_events)

category_count = unique_events.value_counts("category").reset_index()

# st.dataframe(category_count)

col1, col2, col3, a = st.columns(4)

with col2:
    pie_fig = px.pie(
        category_count,
        values="count",
        names="category",
        title=f"Category Distribution in {season} Games all years combined",
        width=600,
        height=400,
    )
    st.plotly_chart(pie_fig)

st.subheader("Category Distribution through the years")
year = st.select_slider("Select the Year", options=unique_events.Year.unique())

category_count_filtered = (
    unique_events[unique_events["Year"] == year].value_counts("category").reset_index()
)

col21, col22, col23, b = st.columns(4)

with col22:
    pie_fig = px.pie(
        category_count_filtered,
        values="count",
        names="category",
        title=f"Category Distribution in {season} Games {year}",
        width=600,
        height=400,
    )
    st.plotly_chart(pie_fig)

st.write(
    "Alongside the gender repartition in the olympic games, we can see that the number of events opened to women has been progressively catching the number of events opened to men"
)

st.subheader("Sport Evolution through the years")

year2 = st.select_slider(
    "Select the Year ", options=games.sort_values("Year").Year.unique()
)

# st.dataframe(games[games["Year"] == year2])

games_event_count = (
    games[games["Year"] == year2]
    .drop_duplicates(subset=["Sport", "Event"])
    .groupby("Sport")["Sport"]
    .value_counts()
    .reset_index()
    .sort_values("count", ascending=False, ignore_index=True)
)
# st.dataframe(games_event_count)

fig = px.bar(
    games_event_count,
    x="Sport",
    y="count",
    color="Sport",
    width=1000,
    height=600,
    labels={"count": "Number of Events"},
    title=f"Number of Events per Sport of the {season} Games {year2}",
)
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)

st.write(
    "The number of events per sport has been increasing since the creation of the olympic games. This can be explained by the creation of new sports, the inclusion of feminine athletes in the olympic games, or the number of weigth categories which can be variable"
)

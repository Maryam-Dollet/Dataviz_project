import streamlit as st
import plotly.express as px
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
    width=1450,
    height=800,
)
fig.update_layout(barmode="stack", xaxis={"categoryorder": "total descending"})
fig.update_xaxes(tickangle=45)

st.plotly_chart(fig)

import streamlit as st
from streamlit_option_menu import option_menu
from cache_func import get_city_position
import plotly.express as px

st.set_page_config(layout="wide")

st.header("Data Visualization of The Olympic Games")

st.subheader("Welcome to our Streamlit !")

st.markdown(
    "For this project, we decided to take advantage of the upcoming Olympic Games to look back at the history of these games and how they have evolved over time."
)
st.markdown(
    "This project allows us both to respond to an issue: the observation of the evolution of sport through the ages."
)
st.markdown(
    "But also to give free rein to our imagination thanks to the incredible variety of information available, and to use the full potential of the plotly.express library."
)

st.markdown("##### We used the following sources:")
st.markdown(
    "- https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results"
)
st.markdown("- https://api-ninjas.com/api/geocoding ")

st.markdown("##### Link to our GitHub:")

st.markdown("https://github.com/Maryam-Dollet/Dataviz_project")

st.markdown("##### Let's open this project with the first visualization:")

st.write(
    "On the sidebar on the left you can navigate through all the pages to see the visualization about the pages' themes."
)

st.write(
    "These are the locations of all the Olympic Games that have taken place since the beginning."
)
st.write(
    "You can change to the Summer or Winter Games on the sidebar (left), you will be able to interact with the visualizations in the same way throughout the pages on differents graphs."
)

with st.sidebar:
    season = option_menu("Choose Season", ["Summer", "Winter"])
df_city_positions = get_city_position(season)

fig = px.scatter_geo(
    df_city_positions,
    lat=df_city_positions.latitude,
    lon=df_city_positions.longitude,
    hover_name="description",
)
fig.update_layout(
    width=1000, height=800, title=f"Host Cities of {season} Games across the years"
)
fig.update_geos(
    bgcolor="#0E1117",
    coastlinecolor="#fff",
    lataxis=dict(showgrid=True, gridwidth=0.2),
    lonaxis=dict(showgrid=True, gridwidth=0.2),
    showcountries=True,
)
fig.update_traces(marker_color="#1E90FF", selector=dict(type="scattergeo"))
fig.update_traces(marker_size=8, selector=dict(type="scattergeo"))

st.plotly_chart(fig)

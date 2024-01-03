import streamlit as st
import plotly.express as px
from cache_func import get_city_position
from streamlit_option_menu import option_menu

st.header("Disciplines")
# season = option_menu("Choose Season", ["Summer", "Winter"], orientation="horizontal")
# df_city_positions = get_city_position(season)
# st.dataframe(df_city_positions)

# fig = px.scatter_geo(df_city_positions,
#                     lat=df_city_positions.latitude,
#                     lon=df_city_positions.longitude,
#                     hover_name="description")
# fig.update_layout(width=1000, height=800)
# st.plotly_chart(fig)

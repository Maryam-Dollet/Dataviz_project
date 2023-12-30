import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_datasets():
    df_athlete = pd.read_csv("athlete_events.csv", sep=",")
    noc_regions = pd.read_csv("noc_regions.csv", sep=",")
    df_merged = df_athlete.merge(noc_regions, how="left", on="NOC")
    return df_merged


df_merged = load_datasets()

st.dataframe(df_merged)

st.subheader("Participans Gender Total")
df1 = (
    df_merged.value_counts("Sex")
    .reset_index()
    .rename(columns={"Sex": "Gender", "count": "gender_count"})
)
st.dataframe(df1)

fig = px.bar(df1, x="Gender", y="gender_count")
st.plotly_chart(fig)

st.subheader("Gender Repartition Through the Years")

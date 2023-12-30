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

st.subheader("Gender Analysis")
df1 = (
    df_merged.value_counts("Sex")
    .reset_index()
    .rename(columns={"Sex": "Gender", "count": "gender_count"})
)
st.dataframe(df1)

fig = px.bar(df1, x="Gender", y="gender_count", title="Gender Repartition")
st.plotly_chart(fig)

st.write("Gender Repartition Through the Years")
df2 = (
    df_merged.groupby("Year")["Sex"]
    .value_counts()
    .reset_index()
    .rename(columns={"count": "nb"})
)

fig = px.bar(
    df2,
    x="Year",
    y="nb",
    color="Sex",
    title="Gender Repartition",
    width=1500,
    height=800,
)
fig.update_xaxes(type="category")
st.plotly_chart(fig)

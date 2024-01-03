import streamlit as st
import pandas as pd
import plotly.express as px
from cache_func import load_datasets


df_merged = load_datasets()

st.header("Athletes Analysis")

st.dataframe(df_merged)

st.subheader("Gender Analysis")
df1 = (
    df_merged.value_counts("Sex")
    .reset_index()
    .rename(columns={"Sex": "Gender", "count": "gender_count"})
)
st.dataframe(df1)

fig = px.bar(
    df1, x="Gender", y="gender_count", title="Gender Repartition", color="Gender"
)
st.plotly_chart(fig)

st.write("Gender Repartition Through the Years")
## False Dataframe groupby, because an athlete can compete in different disciplines in the same year.
df2 = (
    df_merged.groupby(by=["Year", "Name"])["Sex"]
    .value_counts()
    .reset_index()
    .rename(columns={"count": "nb"})
)

df2 = (
    df2.groupby("Year")["Sex"]
    .value_counts()
    .reset_index()
    .rename(columns={"count": "nb_gender", "Sex": "Gender"})
)

st.dataframe(df2.style.format({"Year": lambda x: "{:}".format(x)}))

fig = px.bar(
    df2,
    x="Year",
    y="nb_gender",
    color="Gender",
    title="Gender Repartition",
    barmode="group",
    width=1500,
    height=800,
    text_auto=".2s",
)
fig.update_traces(
    textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
)
fig.update_xaxes(type="category")
st.plotly_chart(fig)

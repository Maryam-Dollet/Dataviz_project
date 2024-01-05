import streamlit as st
import pandas as pd
import plotly.express as px
from cache_func import load_datasets, get_medals_athletes

st.set_page_config(layout="wide")

df_merged = load_datasets()

st.header("Athletes Analysis")

st.dataframe(df_merged)

st.subheader("Gender Analysis")
df1 = (
    df_merged.drop_duplicates(subset=["Year", "ID"])
    .value_counts("Sex")
    .reset_index()
    .rename(columns={"Sex": "Gender", "count": "gender_count"})
)
# st.dataframe(df1)

fig = px.bar(
    df1,
    x="Gender",
    y="gender_count",
    title="Overall Gender Repartition",
    color="Gender",
)
st.plotly_chart(fig)

# st.write("Gender Repartition Through the Years")
## False Dataframe groupby, because an athlete can compete in different disciplines in the same year.
df2 = (
    df_merged.drop_duplicates(subset=["Year", "ID"])
    .groupby("Year")["Sex"]
    .value_counts()
    .reset_index()
    .rename(columns={"count": "nb_gender", "Sex": "Gender"})
)

# st.dataframe(df2.style.format({"Year": lambda x: "{:}".format(x)}))

fig = px.bar(
    df2,
    x="Year",
    y="nb_gender",
    color="Gender",
    title="Gender Repartition through the years",
    barmode="group",
    width=1400,
    height=800,
    text_auto=".2s",
)
fig.update_traces(
    textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
)
fig.update_xaxes(type="category")
st.plotly_chart(fig)

# st.subheader("Number of Athletes per Country over the years")

# no_duplicates = df_merged.drop_duplicates(subset= ['Games', 'ID'])
# games_nd = no_duplicates[no_duplicates.Season == 'Summer']

# athletes_per_country = games_nd.groupby(['Year', 'region']).size().reset_index(name='Nb of athletes')
# st.dataframe(athletes_per_country)

st.subheader("Athletes with the most Medals")

df_athlete_medals = get_medals_athletes()

st.dataframe(df_athlete_medals)

fig = px.bar(
    df_athlete_medals.head(15)[::-1],
    y="Name",
    x=["Gold", "Silver", "Bronze"],
    barmode="stack",
    orientation="h",
    width=1400,
    height=800,
)
# fig.update_layout(yaxis={'categoryorder':'total descending'})
st.plotly_chart(fig)

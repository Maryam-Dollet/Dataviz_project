import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from cache_func import load_datasets, get_medals_athletes

st.set_page_config(layout="wide")

df_merged = load_datasets()

st.header("Athlete Analysis")

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

season = option_menu("Choose Season", ["Summer", "Winter"], orientation="horizontal")

# st.subheader(f"Average Weight and Height per Discipline of {season} Games")

df_merged_season = df_merged[df_merged["Season"] == season]

# df_avg_weight_height_men = (
#     df_merged_season[df_merged_season["Sex"] == "M"]
#     .dropna(subset=["Height", "Weight"])
#     .drop_duplicates(subset=["ID", "Sport"])
#     .groupby("Sport")
#     .agg({"Height": "mean", "Weight": "mean"})
# )
# st.dataframe(df_avg_weight_height_men)

# df_avg_weight_height_women = (
#     df_merged_season[df_merged_season["Sex"] == "F"]
#     .dropna(subset=["Height", "Weight"])
#     .drop_duplicates(subset=["ID", "Sport"])
#     .groupby("Sport")
#     .agg({"Height": "mean", "Weight": "mean"})
# )
# st.dataframe(df_avg_weight_height_women)

st.markdown("#### Men's Height")
df_box_men = (
    df_merged_season[df_merged_season["Sex"] == "M"]
    .dropna(subset=["Height", "Weight"])
    .drop_duplicates(subset=["ID", "Sport"])
)
# st.dataframe(df_box_men)

fig = px.box(df_box_men, x="Sport", y="Height", width=1300, height=800)
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)

st.markdown("#### Men's Weight")

fig = px.box(df_box_men, x="Sport", y="Weight", width=1300, height=800)
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)

st.markdown("#### Women's Height")
df_box_women = (
    df_merged_season[df_merged_season["Sex"] == "F"]
    .dropna(subset=["Height", "Weight"])
    .drop_duplicates(subset=["ID", "Sport"])
)
# st.dataframe(df_box_women)

fig = px.box(df_box_women, x="Sport", y="Height", width=1300, height=800)
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)

st.markdown("#### Women's Weight")

fig = px.box(df_box_women, x="Sport", y="Weight", width=1300, height=800)
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)


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
    title="Top 15 Athletes with the most Medals",
)
# fig.update_layout(yaxis={'categoryorder':'total descending'})
st.plotly_chart(fig)

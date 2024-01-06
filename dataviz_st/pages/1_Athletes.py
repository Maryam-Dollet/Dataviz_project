import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from cache_func import load_datasets, get_medals_athletes

st.set_page_config(layout="wide")

df_merged = load_datasets()

st.header("Athlete Analysis")

# st.dataframe(df_merged)

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
    width=1200,
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
st.subheader("Athletes Height and Weight per Sport")
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

st.markdown(f"#### Men's Height {season} Sports")
df_box_men = (
    df_merged_season[df_merged_season["Sex"] == "M"]
    .dropna(subset=["Height", "Weight"])
    .drop_duplicates(subset=["ID", "Sport"])
)
# st.dataframe(df_box_men)

fig = px.box(df_box_men, x="Sport", y="Height", width=1000, height=600, color="Sport")
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)

st.markdown(f"#### Men's Weight {season} Sports")

fig = px.box(df_box_men, x="Sport", y="Weight", width=1000, height=600, color="Sport")
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)

st.markdown(f"#### Women's Height {season} Sports")
df_box_women = (
    df_merged_season[df_merged_season["Sex"] == "F"]
    .dropna(subset=["Height", "Weight"])
    .drop_duplicates(subset=["ID", "Sport"])
)
# st.dataframe(df_box_women)

fig = px.box(df_box_women, x="Sport", y="Height", width=1000, height=600, color="Sport")
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)

st.markdown(f"#### Women's Weight {season} Sports")

fig = px.box(df_box_women, x="Sport", y="Weight", width=1000, height=600, color="Sport")
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
    width=1000,
    height=600,
    title="Top 15 Athletes with the most Medals",
)
# fig.update_layout(yaxis={'categoryorder':'total descending'})
st.plotly_chart(fig)

st.subheader("Correlation Medal, Height and Weight")

season2 = option_menu("Choose Season ", ["Summer", "Winter"], orientation="horizontal")

filtered_season_df = df_merged[df_merged.Season == season2]

unique_sport = filtered_season_df.Sport.unique()
unique_gender = filtered_season_df.Sex.unique()

option_sport = st.selectbox("Select Sport", tuple(unique_sport))
option_gender = st.selectbox("Select Gender", tuple(unique_gender))

selected_df = filtered_season_df[
    (filtered_season_df.Sport == option_sport)
    & (filtered_season_df.Sex == option_gender)
].dropna(subset=["Age", "Height", "Weight"])

selected_df["Medal"] = selected_df["Medal"].fillna("No medal")

# st.dataframe(selected_df)

if len(selected_df) == 0:
    st.write("No Data")
else:
    correlation_matrix = selected_df[["Age", "Height", "Weight", "Medal"]]

    correlation_matrix["Medal"] = correlation_matrix["Medal"].replace(
        ["No medal", "Gold", "Silver", "Bronze"], [0, 1, 1, 1]
    )

    # st.dataframe(correlation_matrix)

    fig = px.imshow(correlation_matrix.corr(), text_auto=True)
    st.plotly_chart(fig)

    correlation_matrix = (
        correlation_matrix.groupby(["Height", "Weight"])
        .agg({"Medal": "sum", "Height": "count"})
        .rename(columns={"Height": "Nb of athletes"})
        .reset_index()
    )

    correlation_matrix["Proportion of medals"] = (
        correlation_matrix["Medal"] / correlation_matrix["Nb of athletes"]
    )

    correlation_matrix = correlation_matrix[
        correlation_matrix["Proportion of medals"] != 0
    ]

    gtext = "Women" if option_gender == "F" else "Men"

    fig = px.scatter(
        correlation_matrix,
        x="Height",
        y="Weight",
        size="Proportion of medals",
        color="Nb of athletes",
        title=f"Optimal Height and Weight to win a medal in {option_sport} for Athletes competing in the {gtext} Category",
        width=1200,
        height=800,
        color_continuous_scale="plotly3",
    )
    st.plotly_chart(fig)

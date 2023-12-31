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

st.write(
    "We can see that the feminine gender is less represented since the creation of olympic games. Let's dive through the data to explain this representation difference in the following graph :"
)

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

st.write(
    "Since 1896, women were underrepresented in the olympic games, but the emergence of feminine athletes in the olympic games which started in the 20s led to a more and more equal presence of both sexes in the olympic games. It took a century to observe a relative gender equality (numberwise) in the olympic games."
)

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

st.write(
    "We can see a significant difference between the average height of the athletes in the different sports. The average height of the athletes in the sport of basketball is the highest with a median of 195 cm"
)

st.markdown(f"#### Men's Weight {season} Sports")

fig = px.box(df_box_men, x="Sport", y="Weight", width=1000, height=600, color="Sport")
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)

st.write(
    "The weight of the athletes is also very different from one sport to another. We can distinguish a similarity with the previous graph because tall people tend to be heavier (& vice-versa)but there are noticable differences :"
)
st.write(
    "For exemple, in summer games : The average weight of the athletes in the sport of weightlifting is quite high whereas their average height in the previous graph was one of the lowest. This means athletes of this sport are in average stockier people."
)

if season == "Summer":
    st.write(
        "We can also explain, that the Weight of the athletes varies a lot for the following sports: Judo, Weightlifting, Boxing, Wrestling and Athletics. For the contact sports, it is explainable by the fact that the sport events are split into weight categories. As for Athletics, the explanation may be because Athletics is a Sport with a multitude of disciplines that are different from each other and require differents types of bodies to excel in the said discipline. "
    )
else:
    st.write(
        "For the Winter Sports, one noticeabale aspect of the weight graph for both men and women is the Bobsleigh Sport. Both medians (men and women) are high, this could be because the Sport requires a heavy body for an athlete to excel in it. The archetypal (male) bobsledder would be around 190cm talland weigh 105kg so, the hypothesis is well founded"
    )

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

st.write(
    "The average heigth of feminine athletes seems to be lower than the average height of masculine athletes. However, the characteristics of the sports are still present : fe. Basketball or Volleyball stay the sports with the highest average height."
)

st.markdown(f"#### Women's Weight {season} Sports")

fig = px.box(df_box_women, x="Sport", y="Weight", width=1000, height=600, color="Sport")
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)


st.subheader("Athletes with the most Medals")

df_athlete_medals = get_medals_athletes()

st.dataframe(df_athlete_medals)

st.write(
    "The athletes are ranked by the number of medals they won. In case of a tie, the athletes are ranked by the number of gold medals they won etc."
)

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

    st.write(
        "We oberve that for most sports, Height and Weight have a correlation with the number of medals obtained by the athletes. However, this is not automatically the case for all sports. For example, in the sport of Judo, the correlation is very small compared to the sport swimming (~0.03 VS ~0.14)"
    )

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

    st.write(
        "In this last graph, we try to see if there are any optimal height and weight for each sport. "
    )
    st.write(
        "In the graph, the more pink the color is, the more athletes there are with this height and weight."
    )
    st.write(
        "If a circle is big, it means that a high proportion of these athletes have won medals."
    )
    st.write(
        "For readability reasons, we have not displayed the categories of weight and height with a proportion of winning medals equal to 0."
    )

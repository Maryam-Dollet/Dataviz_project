import streamlit as st
import pandas as pd


@st.cache_data
def load_datasets():
    df_athlete = pd.read_csv("athlete_events.csv", sep=",")
    noc_regions = pd.read_csv("noc_regions.csv", sep=",")
    df_merged = df_athlete.merge(noc_regions, how="left", on="NOC")
    return df_merged


@st.cache_data
def get_regions(filter: str):
    df_merged = load_datasets()
    df_merged = df_merged[df_merged["Season"] == filter]
    df = (
        df_merged.drop_duplicates(subset=["Year", "ID"])
        .sort_values("Year")
        .groupby(by=["Year", "region"])["region"]
        .value_counts()
        .reset_index()
        .rename(columns={"count": "participants number"})
    )
    return df


@st.cache_data
def get_city_position(filter: str):
    df_merged = load_datasets()
    city_positions = pd.read_csv("city_position.csv", sep=",")
    df_merged = df_merged.merge(city_positions, how="left", on="City")
    df_merged["description"] = (
        df_merged["City"].astype(str) + " " + df_merged["Year"].astype(str)
    )
    df_merged = (
        df_merged[df_merged["Season"] == filter]
        .drop_duplicates(subset=["City", "Year"])
        .sort_values("Year")
        .reset_index(drop=True)
    )
    return df_merged[["City", "Year", "longitude", "latitude", "description"]]


@st.cache_data
def get_medals(filter: str):
    df_merged = load_datasets()
    df_merged = df_merged[df_merged["Season"] == filter]
    df = (
        df_merged[~df_merged.Medal.isna()]
        .reset_index(drop=True)
        .drop_duplicates(subset=["region", "Year", "Event"])
        .groupby(by=["region", "Year", "Event"])["Medal"]
        .value_counts()
        .reset_index()
        .sort_values("Year")
        .reset_index(drop=True)
        .rename(columns={"count": "medal_count"})
    )

    df_medals = (
        df.pivot_table(
            index=["Year", "region"],
            columns="Medal",
            values="medal_count",
            aggfunc="sum",
        )
        .reset_index()
        .fillna(0)
        .astype({"Gold": "int32", "Silver": "int32", "Bronze": "int32"})
    )
    df_medals["Total"] = df_medals["Bronze"] + df_medals["Gold"] + df_medals["Silver"]

    return df_medals[["Year", "region", "Gold", "Silver", "Bronze", "Total"]]


@st.cache_data
def get_medals_athletes():
    df_merged = load_datasets()
    df = (
        df_merged[~df_merged.Medal.isna()]
        .groupby(by=["ID", "Name"])["Medal"]
        .value_counts()
        .reset_index()
        .rename(columns={"count": "medal_count"})
    )

    df_medals = (
        df.pivot_table(
            index=["ID", "Name"], columns="Medal", values="medal_count", aggfunc="sum"
        )
        .reset_index()
        .fillna(0)
        .astype({"Gold": "int32", "Silver": "int32", "Bronze": "int32"})
    )
    df_medals["Total"] = df_medals["Bronze"] + df_medals["Gold"] + df_medals["Silver"]

    return (
        df_medals[["ID", "Name", "Gold", "Silver", "Bronze", "Total"]]
        .sort_values(by=["Total", "Gold", "Silver", "Bronze"], ascending=False)
        .reset_index(drop=True)
    )


@st.cache_data
def filter_df(df: pd.DataFrame, year: int):
    return df[df["Year"] == year]

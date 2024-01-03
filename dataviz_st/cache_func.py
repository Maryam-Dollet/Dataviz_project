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
        df_merged.drop_duplicates(subset=["Year", "Name"])
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
    df_merged = df_merged[df_merged["Season"] == filter]
    return df_merged

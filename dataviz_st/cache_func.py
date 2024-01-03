import streamlit as st
import pandas as pd


@st.cache_data
def load_datasets():
    df_athlete = pd.read_csv("athlete_events.csv", sep=",")
    noc_regions = pd.read_csv("noc_regions.csv", sep=",")
    df_merged = df_athlete.merge(noc_regions, how="left", on="NOC")
    return df_merged


@st.cache_data
def get_regions():
    df_merged = load_datasets()
    df = (
        df_merged.drop_duplicates(subset=["Year", "Name"])
        .sort_values("Year")
        .groupby(by=["Year", "region"])["region"]
        .value_counts()
        .reset_index()
    )
    return df

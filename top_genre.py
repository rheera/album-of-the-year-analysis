from ast import literal_eval
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
from plotly.figure_factory import create_dendrogram
from scipy.cluster import hierarchy
from sklearn.cluster import AgglomerativeClustering, KMeans

"""
import data
"""
df = pd.read_excel("albums_final.xlsx")
df.info()

"""
cleaning
"""
# drop all rows that don't have genres
df.dropna(subset=["genres"], axis=0, inplace=True)
# convert genres to list
df["genres"] = df["genres"].apply(literal_eval)

# add a new column called primary genre, which is the first genre from the list of genres
df["primary_genre"] = df["genres"].apply(lambda x: x[0] if x else None)


def num_albums_per_genre_year_heat(
    genres_list, start_year=1955, end_year=2025, min_releases=0
):
    """
    Returns a Plotly Heatmap representing the number of albums on the top 100 list of a given year for a cetain genre.
        Parameters
        ----------
        genres_list : list
            List of genres you want to compare. Can be unlimited but the amount of graphs can be messy.
        min_releases : int, optional
            The minimum number of albums a genre has to have on the top 100 in a given year. eg. 7 means that the genre has at least one year where they had 7 albums on the top 100 (default is 0)
        start_year : int, optional
            The first year you want to gather albums from, inclusive (default is 1955)
        last_year : int, optional
            The last year you want to gather albums from, exclusive (default is 2024)

        Returns
        -------
        A Plotly Heatmap.
    """
    df_top_grp = df[
        df["primary_genre"].isin(genres_list)
        & (df["list_year"] >= start_year)
        & (df["list_year"] < end_year)
    ]
    df_grp = df_top_grp.groupby(["primary_genre", "list_year"], as_index=False).count()[
        ["primary_genre", "list_year", "album_name"]
    ]

    df_pivot = df_grp.pivot(
        index="primary_genre", columns="list_year", values="album_name"
    )
    min_albums = min_releases
    df_pivot = df_pivot.loc[df_pivot[df_pivot > min_albums].any(axis=1)]
    df_pivot = df_pivot.fillna(0)

    return px.imshow(
        df_pivot,
        labels=dict(
            x="Year",
            y="Genre",
            color="# of Releases",
        ),
        title="Number of albums in top 100 by Genre per Year",
        height=800,
    )


num_albums_per_genre_year_heat(df["primary_genre"], min_releases=7)


df.head()

# df.to_excel("data_tableau.xlsx")

# df[df["primary_genre"] == "Sequencer & Tracker"]

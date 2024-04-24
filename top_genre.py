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

top_20_genres = (
    df.groupby("primary_genre")
    .count()["album_name"]
    .sort_values(ascending=False)
    .head(20)
)
top_20_genres.index
df_grp = df.groupby(["primary_genre", "list_year"], as_index=False).count()[
    ["primary_genre", "list_year", "album_name"]
]

top_genres = (
    df.groupby("primary_genre").count()["album_name"].sort_values(ascending=False)
)
px.bar(top_genres.head(30))


genres_list = top_genres.head(15).index.to_list() + ["Contemporary R&B", "Neo-Soul"]

df_top_grp = df[df["primary_genre"].isin(genres_list)]
df_grp = df_top_grp.groupby(["primary_genre", "list_year"], as_index=False).count()[
    ["primary_genre", "list_year", "album_name"]
]

df_pivot = df_grp.pivot(index="primary_genre", columns="list_year", values="album_name")
# a genre has to have a minimum number of albums make the list in a single year to be shown
min_albums = 0
df_pivot = df_pivot.loc[df_pivot[df_pivot > min_albums].any(axis=1)]
df_pivot = df_pivot.fillna(0)


px.imshow(
    df_pivot,
    labels=dict(
        x="Year",
        y="Genre",
        color="# of Releases",
    ),
    title="Number of albums in top 100 by Genre per Year",
    height=800,
)


top_genres_2020s = df[df["list_year"] >= 2020]["primary_genre"].value_counts()
top_genres_2020s.head(10).index.to_list()

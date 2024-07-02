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
df = pd.read_excel("AOTY_Top_User_Albums_1955_2024.xlsx")
df.info()

"""
cleaning
"""
# drop all rows that don't have genres
df.dropna(subset=["genres"], axis=0, inplace=True)
df.dropna(subset=["album_length"], axis=0, inplace=True)

df.sort_values("album_length", ascending=False).head()

fig = px.line(df, x="list_year", y="album_length", title="Album Duration Over Time")
fig.show()

df[df["list_year"] == 2015].sort_values("album_length", ascending=False).head()

df_grp = (
    df[
        [
            "list_year",
            "user_score",
            "user_score_float",
            "number_of_ratings",
            "album_length",
            "num_of_tracks",
        ]
    ]
    .groupby("list_year", as_index=False)
    .mean()
)
fig = px.line(
    df_grp,
    x="list_year",
    y=["album_length", "num_of_tracks"],
    title="Album Duration Over Time",
)
fig.show()

df.columns[1:3]

df[df["list_year"] == 1959]["album_length"].describe()
df.info()

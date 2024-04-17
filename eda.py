from ast import literal_eval
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns

# import data
df = pd.read_excel("albums_final.xlsx")
df.info()

# cleaning
# drop all rows that don't have genres
df.dropna(subset=["genres"], axis=0, inplace=True)


# convert genres to list
df["genres"] = df["genres"].apply(literal_eval)

# check how many unique genres there are
genres = df["genres"].to_list()
flat_genres = np.hstack(genres)
len(np.unique(flat_genres))

# Create a co_occurence dictionary of all the genres to see which genres are seen most foten with each other
# Initialize a dictionary to store genre pairs and counts
genre_counts = {}

# Iterate through each row
for genres_list in df["genres"]:
    # Generate all pairs of genres
    pairs = combinations(genres_list, 2)
    for pair in pairs:
        # Update the counts
        genre_counts.setdefault(pair, 0)
        genre_counts[pair] += 1

# Create a DataFrame from the dictionary
co_occurrence_df = pd.DataFrame(
    genre_counts.values(),
    index=pd.MultiIndex.from_tuples(genre_counts.keys()),
    columns=["Count"],
)

# Filter for the top most occuring genres
co_occurrence_top = co_occurrence_df[co_occurrence_df["Count"] > 10].sort_values(
    "Count", ascending=False
)
# Create a pivot table to visualize a heat map
pivot_table = pd.pivot_table(
    co_occurrence_top.reset_index(),
    values="Count",
    index="level_0",
    columns="level_1",
    fill_value=0,
)

# Create a heatmap to visualize the occurences not as a pivot table
plt.figure(figsize=(10, 8))
sns.heatmap(co_occurrence_top, annot=False, cmap="YlGnBu")
plt.title("Genre Co-Occurrence Heatmap")
plt.xlabel("Associated Genre")
plt.ylabel("Genre")
plt.show()


# try and make the same chart as above in plotly
px.imshow(
    co_occurrence_top,
    labels=dict(
        color="# of Occurences",
    ),
    width=400,
    height=1200,
)

# Visualize Pivot Table
px.imshow(
    pivot_table,
    labels=dict(
        x="Genre 2",
        y="Genre 1",
        color="# of Occurences",
    ),
    width=800,
    height=800,
)

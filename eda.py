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
co_occurrence_top = co_occurrence_df[co_occurrence_df["Count"] > 10]
co_occurrence_top.reset_index(inplace=True)
co_occurrence_top.columns = ["Genre 1", "Genre 2", "Count"]
# Create a pivot table to visualize a heat map
pivot_table = pd.pivot_table(
    co_occurrence_top, values="Count", index="Genre 1", columns="Genre 2", fill_value=0
)

# Visualize Pivot Table
plt.figure(figsize=(10, 8))
sns.heatmap(pivot_table, annot=False, cmap="YlGnBu")
plt.title("Genre Co-Occurrence Heatmap")
plt.xlabel("Associated Genre")
plt.ylabel("Genre")
plt.show()

df_3 = co_occurrence_df[co_occurrence_df["Count"] > 10]
pivot_table = pd.pivot_table(
    co_occurrence_df.reset_index(),
    values="Count",
    index="level_0",
    columns="level_1",
    fill_value=0,
)

co_occurrence_df.reset_index()

pivot_table.convert_dtypes().dtypes.value_counts()

pivot_table[pivot_table]

plt.figure(figsize=(10, 8))
sns.heatmap(pivot_table, annot=False, cmap="YlGnBu")
plt.title("Genre Co-Occurrence Heatmap")
plt.xlabel("Associated Genre")
plt.ylabel("Genre")
plt.show()

pivot_table[pivot_table["Abstract Hip Hop"] > 1]

pivot_table = pd.pivot_table(
    df_3.reset_index(), values="Count", index="level_0", columns="level_1", fill_value=0
)

px.imshow(pivot_table)

# occurence table
plt.figure(figsize=(10, 8))
sns.heatmap(df_3, annot=False, cmap="YlGnBu")
plt.title("Genre Co-Occurrence Heatmap")
plt.xlabel("Associated Genre")
plt.ylabel("Genre")
plt.show()

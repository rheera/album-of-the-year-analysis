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
        genre_counts.setdefault(tuple(sorted(pair)), 0)
        genre_counts[tuple(sorted(pair))] += 1
        print(tuple(sorted(pair))) if "Singer-Songwriter" in pair else ""

filtered_genres = {key: value for key, value in genre_counts.items() if value > 20}
sorted_filtered_genres = dict(sorted(filtered_genres.items(), key=lambda item: item[1]))
# Create a DataFrame from the dictionary
co_occurrence_df = pd.DataFrame(
    genre_counts.values(),
    index=pd.MultiIndex.from_tuples(genre_counts.keys()),
    columns=["Count"],
)
list(filtered_genres.keys())[0:5]

l = [(12.2817, 12.2817), (0, 0), (8.52, 8.52)]
list(sum(l, ()))
flattened = [item for sublist in filtered_genres for item in sublist]
unique_filtered_genres = set(flattened)

# Filter for the top most occuring genres
co_occurrence_top = co_occurrence_df[co_occurrence_df["Count"] > 20].sort_values(
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

# Scatter plot of the genre occurences

px.scatter(co_occurrence_top.reset_index(), size="Count", x="level_0", y="level_1")


# new co-occurence matrix
# deprecated method
# u = (pd.get_dummies(pd.DataFrame(genres), prefix='', prefix_sep='')
#        .groupby(level=0, axis=1)
#        .sum())

u = (
    pd.get_dummies(pd.DataFrame(genres), prefix="", prefix_sep="")
    .T.groupby(level=0)
    .sum()
).T


v = u.T.dot(u)
v.values[(np.r_[: len(v)],) * 2] = 0
v_top = v[v > 10]
len(v_top[v_top != np.nan].index)
v_top["Zolo"].T.value_counts()
# v_dropped = v.drop(v[v_top].index)
filtered_df = v[(v > 10).any()]
filtered_df.columns
px.imshow(
    filtered_df,
    labels=dict(
        color="# of Occurences",
    ),
    width=800,
    height=800,
)

# Create co-occurence matrix out of the dictionary of the genre counts
# Extract all unique genres
all_genres = set(genre for pair in sorted_filtered_genres.keys() for genre in pair)

# Initialize an empty matrix (2D list)
num_genres = len(all_genres)
co_occurrence_matrix = [[0] * num_genres for _ in range(num_genres)]

# Fill in the matrix
genre_to_index = {genre: i for i, genre in enumerate(all_genres)}
for (genre1, genre2), count in sorted_filtered_genres.items():
    row, col = genre_to_index[genre1], genre_to_index[genre2]
    co_occurrence_matrix[row][col] = count
    co_occurrence_matrix[col][row] = count  # Symmetric matrix

# Convert to DataFrame (optional)
df_co_occurrence = pd.DataFrame(
    co_occurrence_matrix, index=list(all_genres), columns=list(all_genres)
)

df_co_occurrence = df_co_occurrence.reindex(sorted(df_co_occurrence.columns), axis=1)


# print(df_co_occurrence)
px.imshow(df_co_occurrence.sort_index())


# rummaging through data
df.sort_values("user_score", ascending=False).tail(20)


# clustering


# Convert dictionary values to a numpy array
values = np.array(list(filtered_genres.values())).reshape(-1, 1)

# Initialize KMeans with 2 clusters (you can adjust the number of clusters)
kmeans = KMeans(n_clusters=3, random_state=42)

# Fit KMeans to the data
kmeans.fit(values)

# Get cluster labels for each value
cluster_labels = kmeans.labels_

# Add cluster labels back to the dictionary
for i, key in enumerate(filtered_genres.keys()):
    filtered_genres[key] = cluster_labels[i]

# Print the updated dictionary with cluster labels
print(filtered_genres)

# Trying AgglomerativeClustering

# Create a set of all unique genres
all_genres = set()
for key in genre_counts.keys():
    all_genres.update(key)

# Create a genre-to-index mapping
genre_to_index = {genre: i for i, genre in enumerate(all_genres)}

# Create an empty co-occurrence matrix
co_occurrence_matrix = np.zeros((len(all_genres), len(all_genres)))

# Fill in the co-occurrence matrix
for key, value in genre_counts.items():
    genre1, genre2 = key
    i, j = genre_to_index[genre1], genre_to_index[genre2]
    co_occurrence_matrix[i, j] = value
    co_occurrence_matrix[j, i] = value

# Perform hierarchical clustering
n_clusters = 6
clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward")
cluster_labels = clustering.fit_predict(co_occurrence_matrix)

# Create genre groups based on cluster labels
genre_groups = {i: [] for i in range(n_clusters)}
for genre, label in zip(all_genres, cluster_labels):
    genre_groups[label].append(genre)


all_genres = set(genre for pair in filtered_genres.keys() for genre in pair)

# Initialize an empty matrix (2D list)
num_genres = len(all_genres)
co_occurrence_matrix = [[0] * num_genres for _ in range(num_genres)]

# Fill in the matrix
genre_to_index = {genre: i for i, genre in enumerate(all_genres)}
for (genre1, genre2), count in filtered_genres.items():
    row, col = genre_to_index[genre1], genre_to_index[genre2]
    co_occurrence_matrix[row][col] = count
    co_occurrence_matrix[col][row] = count  # Symmetric matrix

# Convert to DataFrame (optional)
df_co_occurrence = pd.DataFrame(
    co_occurrence_matrix, index=list(all_genres), columns=list(all_genres)
)
# sort the columns alphabetically
df_co_occurrence = df_co_occurrence.reindex(sorted(df_co_occurrence.columns), axis=1)


# print(df_co_occurrence)
px.imshow(
    df_co_occurrence.sort_index(),  # sort the index alphabetically
    width=800,
    height=800,
)


# create_dendrogram(df_co_occurrence.sort_index(), labels=df_co_occurrence.columns)

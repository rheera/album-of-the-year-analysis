from ast import literal_eval
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns

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
        genre_counts.setdefault(pair, 0)
        genre_counts[pair] += 1

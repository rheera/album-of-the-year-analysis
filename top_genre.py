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

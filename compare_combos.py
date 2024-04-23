from ast import literal_eval
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
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


def get_genre_df(genre):
    """
    Gets a DataFrame of album information of albums that contain the genre passed.
        Parameters:
                genre (str): The genre to filter by

        Returns:
                filtered dataframe (DataFrame):
    """
    return df[df["genres"].apply(lambda x: genre in x)]


def genre_total(genre):
    """
    Returns the total number of albums that include a certain genre
        Parameters:
                genre (str): The genre to count

        Returns:
                total albums (int):
    """
    return len(get_genre_df(genre).index)


def genre_releases_by_year(genre, start_year=1955, end_year=2024):
    """
    Returns a DataFrame of a certain genres album releases grouped by release year
        Parameters
        ----------
        genre : str
            The genre you want to filter by
        start_year : int, optional
            The first year you want to gather albums from , inclusive (default is 1955)
        last_year : int, optional
            The last year you want to gather albums from, exclusive (default is 2024)

        Returns
        -------
        grouped_dataframe: DataFrame
            A DataFrame grouping the album releases by year by genre
    """
    genre_df = get_genre_df(genre)
    genre_filtered_df = genre_df[
        (genre_df["list_year"] >= start_year) & (genre_df["list_year"] <= end_year)
    ]
    return genre_filtered_df.groupby("list_year")["album_name"].count()


def compare_genres_releases_by_year(*args, start_year=1955, end_year=2024):
    """
    Returns a plotly line graph comparing the number of album releases a genre by year.
        Parameters
        ----------
        args : str
            The different genres you want to compare. Can be unlimited but the line graph might become messy
        start_year : int, optional
            The first year you want to gather albums from , inclusive (default is 1955)
        last_year : int, optional
            The last year you want to gather albums from, exclusive (default is 2024)

        Returns
        -------
        A plotly line graph
    """
    genre_dfs = []
    for genre in args:
        genre_dfs.append(genre_releases_by_year(genre, start_year, end_year))

    fig_t = go.Figure()

    for genre in args:
        df = genre_releases_by_year(genre, start_year, end_year)
        fig_t.add_scatter(x=df.index, y=df.values, mode="lines", name=genre)
    fig_t.update_layout(
        legend_title_text="Genres",
        legend=dict(x=1, y=1),
        title="Number of Releases by Year per Genre",
    )
    fig_t.show()


compare_genres_releases_by_year(
    "East Coast Hip Hop",
    "Singer-Songwriter",
    "West Coast Hip Hop",
    start_year=1990,
    end_year=2023,
)


def get_genre_top_common_genres(genre, threshold=10, start_year=1955, end_year=2024):
    """
    Returns a DataFrame of a certain genres common genres.
        Parameters
        ----------
        genre : str
            The genre you want to filter by
        threshold : int, optional
            The amount of genres to return in the dataframe (default is 10)
        start_year : int, optional
            The first year you want to gather albums from , inclusive (default is 1955)
        last_year : int, optional
            The last year you want to gather albums from, exclusive (default is 2024)

        Returns
        -------
        top_genres_dataframe: DataFrame
            A DataFrame with the top occuring genres of a certain genre.
    """
    df = get_genre_df(genre)
    genre_filtered_df = df[
        (df["list_year"] >= start_year) & (df["list_year"] <= end_year)
    ]
    genres = genre_filtered_df["genres"].to_list()
    flat_genres = np.hstack(genres)
    genre_df = pd.DataFrame(flat_genres, columns=["genre"])
    top_genres = pd.DataFrame(genre_df.value_counts()).reset_index()
    return top_genres[1 : threshold + 1]


def compare_genres_occurences(*args, threshold=10, start_year=1955, end_year=2024):
    """
    Returns multiple Seaborn heatmaps representing a genre and the amount of times other genres show up alongside it on albums.
        Parameters
        ----------
        args : str
            The different genres you want to compare. Can be unlimited but the amount of graphs can be messy.
        threshold : int, optional
            The amount of genres you want to show on the heatmap (default is 10)
        start_year : int, optional
            The first year you want to gather albums from , inclusive (default is 1955)
        last_year : int, optional
            The last year you want to gather albums from, exclusive (default is 2024)

        Returns
        -------
        A Seaborn figure with multiple heatmaps of the different genres.
    """
    top_1 = get_genre_top_common_genres(args[0], threshold, start_year, end_year)
    num_of_genres = len(args)
    print(num_of_genres)
    fig, axs = plt.subplots(ncols=num_of_genres, figsize=(num_of_genres * 5, 6))

    # Plot the heatmap for genre1
    sns.heatmap(
        top_1.set_index("genre"),
        cmap="YlGnBu",
        annot=True,
        fmt="d",
        cbar=True,
        ax=axs[0],
    )
    axs[0].set_title(f"{args[0]} co-occurence genres")
    axs[0].set_xlabel("")
    axs[0].set_ylabel("Genre")

    # Plot the heatmap for genre2
    for idx, genre in enumerate(args[1:]):
        top_2 = get_genre_top_common_genres(genre, threshold, start_year, end_year)
        sns.heatmap(
            top_2.set_index("genre"),
            cmap="YlGnBu",
            annot=True,
            fmt="d",
            cbar=True,
            ax=axs[idx + 1],
        )
        axs[idx + 1].set_title(f"{genre} co-occurence genres")
        axs[idx + 1].set_xlabel("")
        axs[idx + 1].set_ylabel("")

    plt.tight_layout()
    plt.show()


compare_genres_occurences(
    "Singer-Songwriter", "East Coast Hip Hop", "West Coast Hip Hop", threshold=5
)

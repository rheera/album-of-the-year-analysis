from ast import literal_eval
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import plotly.subplots as sp


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
    return df[df["genres"].apply(lambda x: genre in x)]


def get_genre_cooccurence_plot(genre, genre_threshold):
    df = get_genre_df(genre)
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

    filtered_genres = {
        key: value for key, value in genre_counts.items() if value > genre_threshold
    }
    # sorted_filtered_genres = dict(sorted(filtered_genres.items(), key=lambda item: item[1]))

    # Create a DataFrame from the dictionary
    co_occurrence_df = pd.DataFrame(
        filtered_genres.values(),
        index=pd.MultiIndex.from_tuples(filtered_genres.keys()),
        columns=["Count"],
    )
    # Create a heatmap to visualize the occurences not as a pivot table
    return co_occurrence_df.sort_values("Count", ascending=False)
    # plt.figure(figsize=(10, 8))
    # sns.heatmap(
    #     co_occurrence_df.sort_values("Count", ascending=False),
    #     annot=False,
    #     cmap="YlGnBu",
    # )
    # plt.title("Genre Co-Occurrence Heatmap")
    # plt.ylabel("Genre1-Genre2")
    # return plt

def get_genre_top_common_genres(genre, threshold):
    df = get_genre_df(genre)
    genres = df["genres"].to_list()
    flat_genres = np.hstack(genres)
    genre_df = pd.DataFrame(flat_genres, columns=["genre"])
    top_genres = pd.DataFrame(genre_df.value_counts()).reset_index()
    return top_genres[1:threshold]

east_plot = get_genre_top_common_genres("East Coast Hip Hop", 10)
west_plot = get_genre_top_common_genres("West Coast Hip Hop", 10)

df[df["genres"].apply(lambda x: "East Coast Hip Hop" in x)]
df[df["genres"].apply(lambda x: "East Coast Hip Hop" in x)]


east_plot = get_genre_cooccurence_plot("East Coast Hip Hop", 10)
west_plot = get_genre_cooccurence_plot("West Coast Hip Hop", 10)
east_plot.index
fig, axs = plt.subplots(1, 2, sharey=False)
sns.heatmap(east_plot, annot=False, cmap="YlGnBu", ax=axs[0])
sns.heatmap(west_plot, annot=False, cmap="YlGnBu", ax=axs[1])


# Sample data (replace with your actual data)
df1 = pd.DataFrame(np.random.rand(25, 4), columns=list("ABCD"))
df2 = pd.DataFrame(np.random.rand(25, 4), columns=list("WXYZ"))

# Create a 1x2 grid of subplots
fig, (ax1, ax2) = plt.subplots(ncols=2)
fig.subplots_adjust(wspace=0.01)  # Set small spacing between subplots

# Plot the first heatmap
sns.heatmap(east_plot, x="genre", y="count" cmap="YlGnBu", ax=ax1, cbar=False).set_ylabel("Genre1-Genre2")
px.imshow(east_plot, x="genre", y="count")
# fig.colorbar(ax1.collections[0], ax=ax1, location="left", use_gridspec=False, pad=0.2)
sns.heatmap(east_plot, y="genre", x="count")
# Plot the second heatmap
sns.heatmap(west_plot, cmap="YlGnBu", ax=ax2, cbar=False).set_ylabel("")
# fig.colorbar(ax2.collections[0], ax=ax2, location="right", use_gridspec=False, pad=0.2)
ax2.yaxis.tick_right()
ax2.tick_params(rotation=0)

plt.show()


x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create a 1x2 grid of subplots
fig, axs = plt.subplots(ncols=2, figsize=(10, 4))

# Plot the first line plot
axs[0].plot(east_plot, label="sin(x)", color="b")
axs[0].set_title("Line Plot 1")
axs[0].set_xlabel("x")
axs[0].set_ylabel("y")
axs[0].legend()

# Plot the second line plot
axs[1].plot(west_plot, label="cos(x)", color="r")
axs[1].set_title("Line Plot 2")
axs[1].set_xlabel("x")
axs[1].set_ylabel("y")
axs[1].legend()

plt.tight_layout()
plt.show()


plt.figure(figsize=(8, 6))
sns.heatmap(east_plot, cmap='YlGnBu', annot=True, fmt='d', cbar=True)
plt.title('Genre vs. Count Heatmap')
plt.xlabel('Genre')
plt.ylabel('Count')

plt.show()

plt.pcolor(x=east_plot["genre"], y=east_plot["count"])



# Create a 1-column heatmap
plt.figure(figsize=(6, 8))
sns.heatmap(east_plot.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True)
plt.title('Genre vs. Count Heatmap')
plt.ylabel('Genre')

plt.show()


fig, (ax1, ax2) = plt.subplots(ncols=2)
fig.subplots_adjust(wspace=0.01)  # Set small spacing between subplots

# Plot the first heatmap
# sns.heatmap(east_plot.set_index('genre'), x="genre", y="count" cmap="YlGnBu", ax=ax1, cbar=False)
sns.heatmap(east_plot.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True, ax=ax1)
# fig.colorbar(ax1.collections[0], ax=ax1, location="left", use_gridspec=False, pad=0.2)
# Plot the second heatmap
sns.heatmap(west_plot.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True, ax=ax2).set_ylabel("")
# fig.colorbar(ax2.collections[0], ax=ax2, location="right", use_gridspec=False, pad=0.2)
ax2.yaxis.tick_right()
ax2.tick_params(rotation=0)

plt.show()


fig, axs = plt.subplots(ncols=2, figsize=(12, 6))

# Plot the heatmap for 2021
sns.heatmap(east_plot.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True, ax=axs[0])
axs[0].set_title('Genre vs. Count Heatmap (2021)')
axs[0].set_xlabel('')
axs[0].set_ylabel('Genre')

# Plot the heatmap for 2022
sns.heatmap(west_plot.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True, ax=axs[1])
axs[1].set_title('Genre vs. Count Heatmap (2022)')
axs[1].set_xlabel('')
axs[1].set_ylabel('')

plt.tight_layout()
plt.show()


# Determine the maximum count value across both years
max_count = max(east_plot['count'].max(), west_plot['count'].max())

# Create a 1x2 grid of subplots
fig, axs = plt.subplots(ncols=2, figsize=(12, 6))

# Plot the heatmap for 2021
sns.heatmap(east_plot.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True, ax=axs[0], vmax=max_count)
axs[0].set_title('Genre vs. Count Heatmap (2021)')
axs[0].set_xlabel('Count')
axs[0].set_ylabel('Genre')

# Plot the heatmap for 2022
sns.heatmap(west_plot.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True, ax=axs[1], vmax=max_count)
axs[1].set_title('Genre vs. Count Heatmap (2022)')
axs[1].set_xlabel('Count')
axs[1].set_ylabel('Genre')

plt.tight_layout()
plt.show()



def get_genre_cooccurence_plot(genre, genre_threshold):
    df = get_genre_top_common_genres(genre, genre_threshold)
    sns.heatmap(df.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True)
    plt.xlabel('')
    plt.ylabel('Genre')


e = get_genre_cooccurence_plot("East Coast Hip Hop", 10)  
w = get_genre_cooccurence_plot("West Coast Hip Hop", 10)

fig, axs = plt.subplots(ncols=2, figsize=(12, 6))

# Plot the heatmap for 2021
sns.heatmap(east_plot.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True, ax=axs[0])
axs[0].set_title('Genre vs. Count Heatmap (2021)')
axs[0].set_xlabel('')
axs[0].set_ylabel('Genre')
axs[0] = e
axs[1] = w
# Plot the heatmap for 2022
sns.heatmap(west_plot.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True, ax=axs[1])
axs[1].set_title('Genre vs. Count Heatmap (2022)')
axs[1].set_xlabel('')
axs[1].set_ylabel('')

plt.tight_layout()
plt.show()



fig, axs = plt.subplots(ncols=2, figsize=(12, 6))

# Plot the heatmap for 2021
get_genre_cooccurence_plot("East Coast Hip Hop", 10) 
axs[0].set_title('East Coast Hip Hop Genres')
axs[0].set_xlabel('')
axs[0].set_ylabel('Genre')

# Plot the heatmap for 2022
get_genre_cooccurence_plot("West Coast Hip Hop", 10) 
axs[1].set_title('West Coast Hip Hop Genres')
axs[1].set_xlabel('')
axs[1].set_ylabel('')

plt.tight_layout()
plt.show()

def compare_genres_occurences(genre1, genre2, threshold):
    top_1 = get_genre_top_common_genres(genre1, threshold)
    top_2 = get_genre_top_common_genres(genre2, threshold)
    fig, axs = plt.subplots(ncols=2, figsize=(12, 6))

    # Plot the heatmap for genre1
    sns.heatmap(top_1.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True, ax=axs[0])
    axs[0].set_title(f'{genre1} co-occurence genres')
    axs[0].set_xlabel('')
    axs[0].set_ylabel('Genre')

    # Plot the heatmap for genre2
    sns.heatmap(top_2.set_index('genre'), cmap='YlGnBu', annot=True, fmt='d', cbar=True, ax=axs[1])
    axs[1].set_title(f'{genre2} co-occurence genres')
    axs[1].set_xlabel('')
    axs[1].set_ylabel('')

    plt.tight_layout()
    plt.show()


def genre_total(genre):
    return len(get_genre_df(genre).index)

genre_total("East Coast Hip Hop")
genre_total("West Coast Hip Hop")

compare_genres_occurences("East Coast Hip Hop", "West Coast Hip Hop", 10)

px.bar(df=get_genre_df("East Coast Hip Hop"), x="list_year", y="")
sns.countplot(get_genre_df("East Coast Hip Hop"), x="list_year")

album_counts = get_genre_df("East Coast Hip Hop").groupby("list_year")["album_name"].count()

px.line(album_counts)


album_counts_genre1 = get_genre_df("East Coast Hip Hop").groupby('list_year')['album_name'].count()
album_counts_genre2 = get_genre_df("West Coast Hip Hop").groupby('list_year')['album_name'].count()

fig = px.scatter(x=album_counts_genre1.index, y=album_counts_genre1.values, labels={'x': 'Release Year', 'y': 'Number of Albums'},
              title='Albums Released per Year by Genre')
fig.add_scatter(x=album_counts_genre2.index, y=album_counts_genre2.values, mode='lines')
fig.update_traces(showlegend=True, name="Genre1, genre2")
fig.update_layout(
    legend_title_text='Genres',
    legend=dict(x=1, y=1)  # Position the legend at the top-left corner
    
)
fig.show()

fig_t = go.Figure()
fig_t.add_scatter(x=album_counts_genre1.index, y=album_counts_genre1.values, mode='lines', name="Genre1")
fig_t.add_scatter(x=album_counts_genre2.index, y=album_counts_genre2.values, mode='lines', name="Genre2")
fig_t.update_layout(
    legend_title_text='Genres',
    legend=dict(x=1, y=1),
    title="Testtttt"
)
fig_t.show()

def genre_releases_by_year(genre, start_year=1955, end_year=2024):
    genre_df = get_genre_df(genre)
    genre_filtered_df = genre_df[(genre_df['list_year'] >= start_year) & (genre_df['list_year'] <= end_year)]
    return genre_filtered_df.groupby('list_year')['album_name'].count()

def compare_genres_releases_by_year(*args, start_year=1955, end_year=2024):

    genre_dfs = []
    for genre in args:
        genre_dfs.append(genre_releases_by_year(genre, start_year, end_year))

    fig_t = go.Figure()

    for genre in args:
        df = genre_releases_by_year(genre, start_year, end_year)
        fig_t.add_scatter(x=df.index, y=df.values, mode='lines', name=genre)
    fig_t.update_layout(
        legend_title_text='Genres',
        legend=dict(x=1, y=1),
        title="Number of Releases by Year per Genre"
    )
    fig_t.show()

compare_genres_releases_by_year("East Coast Hip Hop", "Singer-Songwriter","West Coast Hip Hop", start_year=1990, end_year=2023)

# import os

# import discogs_client
# import pandas as pd

# from dotenv import load_dotenv

# load_dotenv()

# d = discogs_client.Client(
#     os.environ.get("USER_AGENT"), user_token=os.environ.get("DISCOGS_TOKEN")
# )


def get_album_track_info(all_results, album_name, artist_name):
    """Get an album's track info from Discogs Results.

    Parameters
    ----------
    all_results : discogs_client.models.MixedPaginatedList
        List of results from the search made for an album using the Discogs API.
    album_name : str
        Name of the album searched for.
    artist_name : str
        Name of the artist searched for.

    Returns
    -------
    album_data : {'num_of_tracks': (int, None) , 'album_length': int}
        If there is no information of (ie. no number of tracks) it will return None. Otherwise a dict with keys "num_of_tracks" and "album_length".

    """
    import re
    from statistics import mode

    from add_album_data_util_funcs import duration_str_to_mins
    
    album_tracks = None
    album_length = 0
    # this list keeps track of all the number of track lengths of each release and we will return the value the shows up most often if we don't get a release that contains track durations
    album_tracks_list = []
    for release in all_results:
        try:
            # A lot of Discogs releases have the title start with the artist name, so remove that
            title = release.title.removeprefix(artist_name)
            # if the album name from discogs and the one we're looking for isn't the same go to the next release
            if (
                re.sub(r"[\W_]+", "", title).lower()
                != re.sub(r"[\W_]+", "", album_name).lower()
            ):
                continue
            album_tracks_list.append(len(release.tracklist))
            for track_idx, track in enumerate(release.tracklist):
                if track.duration in ("", None, 0):
                    album_length = 0
                    break
                else:
                    album_length += duration_str_to_mins(track.duration)
                    # if we've gone through all the tracks then we can stop looping and return our track data
                    if track_idx == len(release.tracklist) - 1:
                        album_tracks = len(release.tracklist)
                        break
        except Exception as ex:
            # if type(ex).__name__ == "HTTPError":
            if ex.status_code == 429:
                raise ex
            continue
        if album_length > 0:
            break
    return {
        # return the most common number of tracks if we don't have one with a length
        "num_of_tracks": (
            mode(album_tracks_list)
            if (album_tracks == None and album_tracks_list)
            else album_tracks
        ),
        "album_length": album_length,
    }


def get_album_data(discog_client, album_name, album_artist, album_year=""):
    """Gets the number of tracks and length of an album.

    Searches for releases from Discogs API. Then calls get_album_track_info on the releases.

    Parameters
    ----------
    album_name : str
        Name of the album to search for.
    album_artist : str
        Name of the artist to search for.
    year : str, optional
        Year the album was released

    Returns
    -------
    new_album_data : None, {'num_of_tracks': int, 'album_length': int}
        If there is no information of (ie. no number of tracks) it will return None. Otherwise a dict with keys "num_of_tracks" and "album_length".
    """
    new_album_data = None
    # first check releases that are masters, if they don't have enough information then check all releases 
    all_results = discog_client.search(
        artist=album_artist, type="master", release_title=album_name, year=album_year
    )
    if all_results.count != None and all_results.count > 0:
        new_album_data = get_album_track_info(all_results, album_name, album_artist)
    if (
        all_results.count == 0
        or new_album_data == None
        or new_album_data["album_length"] == 0
    ):
        all_results = discog_client.search(
            artist=album_artist,
            type="release",
            release_title=album_name,
            year=album_year,
        )
    if all_results.count == 0:
        return None
    new_album_data = get_album_track_info(all_results, album_name, album_artist)
    if new_album_data["num_of_tracks"] == None:
        return None
    else:
        return new_album_data


def get_additional_data_range(discog_client, start_df):
    """Returns original DataFrame with additional album data added.

    Searches for releases from Discogs API. Then calls get_album_track_info on the releases. Returns the DataFrame with the added data

    Parameters
    ----------
    discogs_client : discogs_client.client.Client
        A Discog Client object with the user's USER agent and token.
    start_df : DataFrame
        The DataFrame of album data that will be used to get the additional data

    Returns
    -------
    start_df : DataFrame
        Returns the original DataFrame with two extra columns: album_length, and num_of_tracks. 
    """
    import time

    import pandas as pd
    for idx, row in start_df.iterrows():
        time.sleep(3)
        try: 
            album_data = get_album_data(discog_client, row["album_name"], row["artist_name"], row["list_year"])
            if album_data == None:
                continue
            else:
                start_df.loc[idx, 'album_length'] = album_data["album_length"]
                start_df.loc[idx, 'num_of_tracks'] = album_data["num_of_tracks"]

        except Exception as ex:
            print(ex)
            # if ex.status_code == 429:
            with open("log.csv", "a") as logFile:
                logFile.write(f"{row["album_name"]}, {row["artist_name"]}, {row["list_year"]}, {ex.args}\n")
            break;
            # else:
            #     continue
    return start_df


def write_additional_data(discogs_client, start_df):
    """Writes a DataFrame with the additional data to an excel file.

    Searches for releases from Discogs API. Then calls get_album_track_info on the releases. Then writes the data to an excel file.

    Parameters
    ----------
    discogs_client : discogs_client.client.Client
        A Discog Client object with the user's USER agent and token.
    start_df : DataFrame
        The DataFrame of album data that will be used to get the additional data

    Returns
    -------
    Void: Creates or appends to an excel file named albums_data_added.xlsx with the new information (album length and number of tracks) and the old album information. 
    """
    import pandas as pd
    new_df = get_additional_data_range(discogs_client, start_df)
    # new_df.to_csv('added_data.csv', mode='a', index=False, header=False)
    with pd.ExcelWriter("albums_data_added.xlsx", mode="a", if_sheet_exists="overlay") as writer:
        new_df.to_excel(writer, sheet_name="Sheet1", header=None,
                index=False, startrow=writer.sheets["Sheet1"].max_row)  
        



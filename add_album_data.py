import os

import discogs_client
import pandas as pd
from dotenv import load_dotenv

from add_album_data_util_funcs import duration_str_to_mins

load_dotenv()


d = discogs_client.Client(
    os.environ.get("USER_AGENT"), user_token=os.environ.get("DISCOGS_TOKEN")
)

results = d.search(
    artist="Miles Davis", type="release", release_title="Blue Moods", year="1955"
)

country = results.__getitem__(0).country
num_of_tracks = len(results.__getitem__(0).tracklist)
album_length = 0
for track in results.__getitem__(0).tracklist:
    print(track.duration)
    album_length += duration_str_to_mins(track.duration)
results.__getitem__(0).artists[0].profile
num_of_members = len(results.__getitem__(0).artists[0].members)

results.__getitem__(0).artists_sort


def get_album_track_data(album_result):
    album_length = 0
    for track in album_result.tracklist:
        album_length += duration_str_to_mins(track.duration)
    return {
        "num_of_tracks": len(album_result.tracklist),
        "album_length": album_length,
    }


results = d.search(
    artist="MGMT", type="release", release_title="Loss of Life", year="2024"
)
results.__getitem__(0)
get_album_track_data(results.__getitem__(0))

results.__getitem__(1).tracklist[9].duration

results.__iter__()
good_idx = None
for idx, release in enumerate(results):
    for track_idx, track in enumerate(release.tracklist):
        if track.duration in ("", None, 0):
            break
        else:
            if track_idx == len(release.tracklist):
                good_idx = idx
            break


def get_good_album_release(all_results):
    good_idx = None
    for idx, release in enumerate(all_results):
        # print(release)
        for track_idx, track in enumerate(release.tracklist):
            # print(track)
            if track.duration in ("", None, 0):
                break
            else:
                if track_idx == len(release.tracklist) - 1:
                    good_idx = idx
                    break
        if good_idx != None:
            break
    return good_idx


good_album_id = get_good_album_release(results)


get_album_track_data(results.__getitem__(good_album_id))


def get_album_data(album_name, album_artist, album_year):
    all_results = d.search(
        artist=album_artist, type="release", release_title=album_name, year=album_year
    )
    good_album_id = get_good_album_release(all_results)
    return (
        get_album_track_data(all_results.__getitem__(good_album_id))
        if good_album_id != None
        else None
    )

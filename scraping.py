import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

cache_link = "https://webcache.googleusercontent.com/search?q=cache:https://www.albumoftheyear.org/ratings/user-highest-rated/2024/"

r = requests.get(cache_link)
soup = BeautifulSoup(r.text, features="html.parser")


album_list = soup.find_all(class_="albumListRow")
rank = int(float(album_list[1].find(class_="albumListRank").text))
title = album_list[1].find(class_="albumListTitle").text
artist_name = re.search(r"[\d]+[\.](.*)-", title).group(1).strip()
album_name = re.search(r"[\d]+[\.].+-(.*)", title).group(1).strip()
release_date = album_list[1].find(class_="albumListDate").text
genres = album_list[1].find(class_="albumListGenre").text.split(", ")
user_score = int(album_list[6].find(class_="scoreValue").text)
user_score_float = float(
    album_list[6].find(class_="scoreValueContainer").attrs["title"]
)
number_of_ratings = int(
    album_list[2].find(class_="scoreText").text.split(" ")[0].replace(",", "")
)
link_to_album = album_list[1].find("a", itemprop="url").attrs["href"]


def check_must_hear(album_cover_classes):
    if "mustHear" in album_cover_classes:
        if "both" in album_cover_classes:
            return "both"
        elif "user" in album_cover_classes:
            return "user"
        else:
            return "critic"
    else:
        return "no"


# must_hear = check_must_hear(album_list[5].find(class_="albumListCover").attrs["class"])
# type(album_list[1])


def get_album_info(album_element):
    rank = int(float(album_element.find(class_="albumListRank").text))
    title = album_element.find(class_="albumListTitle").text
    artist_name = re.search(r"[\d]+[\.](.*)-", title).group(1).strip()
    album_name = re.search(r"[\d]+[\.].+-(.*)", title).group(1).strip()
    release_date = album_element.find(class_="albumListDate").text
    genres = album_element.find(class_="albumListGenre").text.split(", ")
    user_score = int(album_element.find(class_="scoreValue").text)
    user_score_float = float(
        album_element.find(class_="scoreValueContainer").attrs["title"]
    )
    number_of_ratings = int(
        album_element.find(class_="scoreText").text.split(" ")[0].replace(",", "")
    )
    link_to_album = album_element.find("a", itemprop="url").attrs["href"]
    must_hear = check_must_hear(
        album_element.find(class_="albumListCover").attrs["class"]
    )

    return {
        "rank": rank,
        "artist_name": artist_name,
        "album_name": album_name,
        "release_date": release_date,
        "genres": genres,
        "user_score": user_score,
        "user_score_float": user_score_float,
        "number_of_ratings": number_of_ratings,
        "link_to_album": link_to_album,
        "must_hear": must_hear,
    }


albums_list = []
for album in album_list:
    albums_list.append(get_album_info(album))
get_album_info(album_list[20])

df = pd.DataFrame(albums_list)

album_info = {
    "ranking": 1,
    "artist_name": "art",
    "album_name": "alb",
    "release_date": "oct 22, 2021",
    "genres": ["gen1", "gen2"],
    "user_score": 91,
    "number_of_ratings": 4333,
    "link": ".com",
    "must_hear": "both",
}

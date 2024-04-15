import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

base_url = "https://webcache.googleusercontent.com/search?q=cache:https://www.albumoftheyear.org/ratings/user-highest-rated/"
# year_url = "1958/"
# page_url = "4/"

r = requests.get(base_url + year_url + page_url)
soup = BeautifulSoup(r.text, features="html.parser")
r.status_code

album_list = soup.find_all(class_="albumListRow")
rank = int(float(album_list[0].find(class_="albumListRank").text))
title = album_list[15].find(class_="albumListTitle").text
artist_name = re.search(r"[\d]+[\.](.*)-", title).group(1).strip()
album_name = re.search(r"[\d]+[\.].+-(.*)", title).group(1).strip()
release_date = album_list[0].find(class_="albumListDate").text
genres = (
    album_list[0].find(class_="albumListGenre").text.split(", ")
    if album_list[0].find(class_="albumListGenre")
    else ""
)
user_score = int(album_list[6].find(class_="scoreValue").text)
user_score_float = float(
    album_list[6].find(class_="scoreValueContainer").attrs["title"]
)
number_of_ratings = int(
    album_list[2].find(class_="scoreText").text.split(" ")[0].replace(",", "")
)
link_to_album = album_list[1].find("a", itemprop="url").attrs["href"]
list_year = int(year_url[0:4])
album_artwork_link = (
    album_list[0].find(class_="albumListCover").find("img").attrs["data-src"]
)
type(album_list[2])


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


def get_album_info(album_element, list_year):
    rank = int(float(album_element.find(class_="albumListRank").text))
    title = album_element.find(class_="albumListTitle").text
    artist_name = re.search(r"[\d]+[\.](.*)-", title).group(1).strip()
    album_name = re.search(r"[\d]+[\.].+-(.*)", title).group(1).strip()
    release_date = album_element.find(class_="albumListDate").text
    genres = (
        album_element.find(class_="albumListGenre").text.split(", ")
        if album_element.find(class_="albumListGenre")
        else ""
    )
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
    album_artwork_link = (
        album_element.find(class_="albumListCover").find("img").attrs["data-src"]
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
        "album_artwork_link": album_artwork_link,
        "list_year": list_year,
    }


albums_list = []
for album in album_list:
    albums_list.append(get_album_info(album, int(year_url[0:4])))
# get_album_info(album_list[20])


def get_years_top_albums(base_url, year_url):
    years_album_list = []
    for page_number in range(1, 5):
        page_url = str(page_number) + "/"
        if page_number == 1:
            page_url = ""
        r = requests.get(base_url + year_url + page_url)
        if r.status_code == 404:
            continue
        soup = BeautifulSoup(r.text, features="html.parser")
        album_list = soup.find_all(class_="albumListRow")
        for album in album_list:
            years_album_list.append(get_album_info(album, int(year_url[0:4])))
    return years_album_list


for page_number in range(1, 5):
    page_url = str(page_number) + "/"
    if page_number == 1:
        page_url = ""
    r = requests.get(base_url + year_url + page_url)
    if r.status_code == 404:
        continue
    soup = BeautifulSoup(r.text, features="html.parser")
    album_list = soup.find_all(class_="albumListRow")
    for album in album_list:
        albums_list.append(get_album_info(album, int(year_url[0:4])))


def get_range_top_albums(start_year, end_year, base_url):
    full_albums_list = []
    for year_number in range(start_year, end_year):
        year_url = str(year_number) + "/"
        full_albums_list = full_albums_list + get_years_top_albums(base_url, year_url)
    return full_albums_list


test = get_range_top_albums(1955, 1958, base_url)

albums_1955_to_1965 = []
for year_number in range(1955, 1958):
    year_url = str(year_number) + "/"
    albums_1955_to_1965 = albums_1955_to_1965 + get_years_top_albums(base_url, year_url)
df = pd.DataFrame(albums_1955_to_1965)
df.head()
decade_albums[0:2]
df[df["list_year"] == 1957]

albums_1958 = get_years_top_albums(base_url, "1958/")

df = pd.DataFrame(albums_1958)
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

import time

time.sleep(5)

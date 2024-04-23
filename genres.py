import json
import os

import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from scraping_functions_bypass import (
    create_session,
    get_album_info,
    get_flare_response,
    get_range_top_albums,
    get_years_top_albums,
)

load_dotenv()

flare_url = os.environ.get("flare_url")
session_url = "https://www.albumoftheyear.org/"
base_url = "https://www.albumoftheyear.org/genre/list.php"

session_id = create_session(flare_url, base_url)
r = get_flare_response(flare_url, session_id, base_url)
soup = BeautifulSoup(r["text"], features="html.parser")
genres_cnt = soup.find_all(class_="genreList")
genres_divs = genres_cnt[0].findChildren("div")
all_parent_genres = []
write_genre = {"genres": []}
for genre in genres_divs:
    if len(genre.findChildren("a")) > 1:
        write_genre["genres"].append(
            {"genre": genre.findChildren("a")[0].text, "children": []}
        )
    else:
        write_genre["genres"].append({"genre": genre.findChildren("a")[0].text})
len(all_parent_genres)
for genre in all_parent_genres:
    write_genre["genres"].append({"genre": genre})
with open("genres_flat.json", "w", encoding="utf-8") as f:
    json.dump(write_genre, f, ensure_ascii=False, indent=4)

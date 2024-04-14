import requests
from bs4 import BeautifulSoup

from scraping_functions import (
    get_album_info,
    get_range_top_albums,
    get_years_top_albums,
)

base_url = "https://webcache.googleusercontent.com/search?q=cache:https://www.albumoftheyear.org/ratings/user-highest-rated/1957/2/"

r = requests.get(base_url)
soup = BeautifulSoup(r.text, features="html.parser")
r.headers
r.text
album_list = soup.find_all(class_="albumListRow")

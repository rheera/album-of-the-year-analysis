import pandas as pd
import requests
from bs4 import BeautifulSoup

from scraping_functions import (
    get_album_info,
    get_range_top_albums,
    get_years_top_albums,
)

# test if get_album_info works
sinlge_album_url = "https://webcache.googleusercontent.com/search?q=cache:https://www.albumoftheyear.org/ratings/user-highest-rated/1958/3/"

r = requests.get(sinlge_album_url)
soup = BeautifulSoup(r.text, features="html.parser")
# r.headers
# r.text
album_list = soup.find_all(class_="albumListRow")
test_album = album_list[2]
test_album_info = get_album_info(test_album, 1958)

# test if get_years_top_albums works
base_url = "https://webcache.googleusercontent.com/search?q=cache:https://www.albumoftheyear.org/ratings/user-highest-rated/"

test_1958_albums = get_years_top_albums(base_url, "1958/")
test_1958_df = pd.DataFrame(test_1958_albums)
# test if get_range_top_albums works
decade_1955_1964 = get_range_top_albums(1955, 1965, base_url)
decade_1955_1964_df = pd.DataFrame(decade_1955_1964)

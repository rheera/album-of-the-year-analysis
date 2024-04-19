import os

import pandas as pd
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

session_id = create_session(
    flare_url,
)

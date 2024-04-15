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
base_url = "https://www.albumoftheyear.org/ratings/user-highest-rated/"
sinlge_album_url = "https://www.albumoftheyear.org/ratings/user-highest-rated/1958/3/"
session_id = create_session(flare_url, session_url)
# session_id = "7d02ccad-fb40-11ee-a80d-7085c2fc3ee3"
test_1958_albums = get_years_top_albums(flare_url, session_id, base_url, "1958/")
test_1958_df = pd.DataFrame(test_1958_albums)

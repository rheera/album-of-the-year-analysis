import os
import time

import discogs_client
import pandas as pd
from dotenv import load_dotenv

from add_album_data import write_additional_data

load_dotenv()

d = discogs_client.Client(
    os.environ.get("USER_AGENT"), user_token=os.environ.get("DISCOGS_TOKEN")
)


df = pd.read_excel("albums_final.xlsx")

for i in range(1955, 2025):
    df_sample = df[df["list_year"] == i].copy()
    write_additional_data(d, df_sample)
    print(i)
    time.sleep(60)

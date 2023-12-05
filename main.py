import json
import os
import time
import http.client
import pickle
import pandas as pd
from os.path import expanduser
from dotenv import dotenv_values
from tqdm import tqdm

# Configuration and setup
home = expanduser("~")
scrape_it_config = dotenv_values(os.path.join(home, "creds", "scrape-it.env"))
conn = http.client.HTTPSConnection("api.scrape-it.cloud")

# Variables for scraping
zone = "zarate"
coords = "@-34.106385,-59.082982,13z"

# Scraping loop
df_dict = {}
for i in tqdm(range(0, 10)):
    payload = json.dumps({
        "country": "BR",
        "domain": "com",
        "keyword": "maderera",
        "start": 20 * i,
        "ll": coords,
    })
    headers = {
        'x-api-key': scrape_it_config["API_KEY"],
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/scrape/google/locals", payload, headers)
    res = conn.getresponse()
    data = res.read()
    new_data = data.decode("utf-8")
    result = json.loads(new_data)
    df = pd.DataFrame(result["scrapingResult"]['locals'])
    df_dict[f'{zone}_{i}'] = df

    # Saving results to files
    with open(os.path.join("jsons", f'madereras_{zone}_{i}.json'), 'w') as outfile:
        json.dump(result, outfile)
    with open(os.path.join("dicts", f'madereras_dict{zone}.pkl'), 'wb') as outfile:
        pickle.dump(df_dict, outfile)
    
    joined_df = pd.concat(df_dict.values())
    joined_df.to_excel(os.path.join("dfs", f"madereras_{zone}.xlsx"))

    if len(result["scrapingResult"]['locals']) < 20:
        print(f"Finished scraping {zone} at {i} iteration")
        break

    time.sleep(2)

# Aggregating results from saved files
joined_dict = {}
for path, subdirs, files in os.walk("dicts"):
    for name in files:
        with open(os.path.join(path, name), "rb") as file:
            current_dict = pickle.load(file)
            joined_dict.update(current_dict)

joined_df = pd.concat(joined_dict.values())
joined_df.drop_duplicates(subset=["placeId"], inplace=True)
joined_df.to_excel("madereras_total_sin_duplicados.xlsx")

# Data transformation
columns = [
    "title", "address", "placeId", "website", "gpsCoordinates", "phone", "type", "rating", "workingHours"
]
dict_cols = ["gpsCoordinates", "workingHours"]
joined_df = joined_df[columns]

for column in dict_cols:
    joined_df[column] = joined_df[column].apply(json.dumps).astype(str)

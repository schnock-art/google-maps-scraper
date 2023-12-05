#%%
import logging
import logging.config
import os
import time
from os.path import expanduser
from dotenv import dotenv_values
from tqdm import tqdm
import http.client
import json
import os 

import pickle 
import pandas as pd
home = expanduser("~")
#base_dir = os.path.join(home, "Documents", "libros", "arxiv")
scrape_it_config = dotenv_values(os.path.join(home, "creds", "scrape-it.env"))
#%%


#%%
#for i in range(2, 10):
#%%
df_dict = {}
conn = http.client.HTTPSConnection("api.scrape-it.cloud")
zone = "mar_del_plata"
coords = "@-38.0174516,-57.7653418,11z"

for i in tqdm(range(0, 10)):

    payload = json.dumps({
        "country": "BR",
        "domain": "com",
        "keyword": "maderera",
        "start": 20*i,
        "ll": coords,
    })
    headers = {
    'x-api-key': scrape_it_config["API_KEY"],
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/scrape/google/locals", payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    new_data =data.decode("utf-8")
    result = json.loads(new_data)
    df = pd.DataFrame(result["scrapingResult"]['locals'])
    df_dict[f'{zone}_{i}'] = df
    with open(
        os.path.join("jsons",
                     f'madereras_{zone}_{i}.json'
                     ), 'w') as outfile:
        json.dump(result, outfile)
    with open(os.path.join("dicts",
                           f'madereras_dict{zone}.pkl'
                           ), 'wb') as outfile:
        pickle.dump(df_dict, outfile)
    joined_df=pd.concat([df for df in df_dict.values()])
    joined_df.to_excel(os.path.join("dfs",f"madereras_{zone}.xlsx"))
    if len(result["scrapingResult"]['locals']) < 20:
        print(f"Finished scraping {zone} at {i} iteration")
        break

    time.sleep(2)

# %%
joined_dict = {}
for path, subdirs, files in os.walk("dicts"):
    for name in files:
        with open(os.path.join(path, name), "rb") as file:
            current_dict = pickle.load(file)
            joined_dict.update(current_dict)
# %%
joined_df=pd.concat([df for df in joined_dict.values()])

# %%

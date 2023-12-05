import json
import os
import time
import http.client
import pickle
from typing import Any
import pandas as pd
from os.path import expanduser
from dotenv import dotenv_values
from tqdm import tqdm
import argparse
import logging


def parse_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument('--zone', type=str, default='zarate')
        parser.add_argument('--coords', type=str, default='@-34.106385,-59.082982,13z')
        parser.add_argument('--query', type=str, default='maderera')
        parser.add_argument('--country', type=str, default='BR')
        parser.add_argument('--domain', type=str, default='com')
        parser.add_argument('--start', type=int, default=0)
        parser.add_argument('--end', type=int, default=1)
        parser.add_argument('--output_file', type=str, default='deduplicated_results.xlsx')
        parser.add_argument('--output_dir', type=str, default=None)
        parser.add_argument('--scrape_env_dir', type=str, default='creds')
        return parser.parse_args()

class GoogleMapsScraper:
    def __init__(self, args):
        self.args = args
        self.initialize_logging()
        self.create_output_directories()
        self.scrape_it_config = self.get_scrape_config()

    def initialize_logging(self, level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        return
    

    def create_output_directories(self):
        self.logger.info("Creating subdirectories")
        if self.args.output_dir is not None:
            if not os.path.exists(self.args.output_dir):
                self.logger.info(f"Creating output directory {self.args.output_dir}")
                os.mkdir(self.args.output_dir)
            self.output_file = os.path.join(self.args.output_dir, self.args.output_file)
        else:
            self.output_file = self.args.output_file
        
        output_subdirs = ["dfs", "dicts", "jsons"]
        self.output_dirs = {}
        for subdir in output_subdirs:
            if self.args.output_dir is not None:
                self.output_dirs[subdir] = os.path.join(self.args.output_dir, subdir)
            else:
                self.output_dirs[subdir] = subdir
            os.makedirs(self.output_dirs[subdir], exist_ok=True)

    def get_scrape_config(self):
        self.logger.info("Loading scrape config")
        home = expanduser("~")
        return dotenv_values(os.path.join(home, self.args.scrape_env_dir, "scrape-it.env"))


    def scrape_data(self):
        self.logger.info("Scraping data")
        conn = http.client.HTTPSConnection("api.scrape-it.cloud")
        self.current_df_dict = {}
        for i in tqdm(range(self.args.start, self.args.end)):
            payload = json.dumps({
                "country": self.args.country,
                "domain": self.args.domain,
                "keyword": self.args.query,
                "start": 20 * i,
                "ll": self.args.coords,
            })
            headers = {
                'x-api-key': self.scrape_it_config["API_KEY"],
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/scrape/google/locals", payload, headers)
            res = conn.getresponse()
            data = res.read()
            new_data = data.decode("utf-8")
            result = json.loads(new_data)
            df = pd.DataFrame(result["scrapingResult"]['locals'])
            self.current_df_dict[f'{self.args.zone}_{i}'] = df

            # Saving results to files
            self.logger.info(f"Saving iteration {i} results to files")
            with open(os.path.join(self.output_dirs["jsons"], f'{self.args.query}_{self.args.zone}_{i}.json'), 'w') as outfile:
                json.dump(result, outfile)
            with open(os.path.join(self.output_dirs["dicts"], f'{self.args.query}_dict_{self.args.zone}.pkl'), 'wb') as outfile:
                pickle.dump(self.current_df_dict, outfile)
            
            joined_df = pd.concat(self.current_df_dict.values())
            joined_df.to_excel(os.path.join(self.output_dirs["dfs"], f"{self.args.query}_{self.args.zone}.xlsx"))

            if len(result["scrapingResult"]['locals']) < 20:
                self.logger.info(f"Finished scraping {self.args.zone} at {i} iteration")
                break

            time.sleep(2)
        return self.current_df_dict
    
    def aggregate_results(self):
        self.logger.info("Aggregating results")
        #Aggregating results from saved files
        self.joined_dict = {}
        for path, subdirs, files in os.walk(self.output_dirs["dicts"]):
            for name in files:
                with open(os.path.join(path, name), "rb") as file:
                    self.logger.info(f"Loading {os.path.join(path, name)}")
                    current_dict = pickle.load(file)
                    self.joined_dict.update(current_dict)
        return self.joined_dict
    
    def save_final_results(self):
        self.logger.info("Saving final results")
        # Save final results logic...
        self.joined_df = pd.concat(self.joined_dict.values())
        self.joined_df.drop_duplicates(subset=["placeId"], inplace=True)
        self.joined_df.to_excel(self.output_file)

###
if __name__ == "__main__":
    args = parse_arguments()
    scraper = GoogleMapsScraper(args)
    try:
        scraper.scrape_data()
        scraper.aggregate_results()
        scraper.save_final_results()
        scraper.logger.info("Finished scraping succesfully!")
    except Exception as e:
        scraper.logger.error(f"Error while scraping: {e}")
        raise e

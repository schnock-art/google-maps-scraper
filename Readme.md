# Google Maps Scraper

## Overview
This script is designed to scrape data from Google Maps using specific keywords, geographic coordinates, and other parameters. It allows users to gather data from Google Maps listings, which can include details like the name, address, and contact information of businesses or places.

## Features
- Scrapes Google Maps data based on user-defined parameters.
- Saves individual and aggregated scraping results in different formats including JSON, Excel, and Pickle.
- Utilizes command-line arguments for flexible configuration.
- Includes logging for easy tracking and debugging of the scraping process.

## Requirements
- Python 3.x
- Required Python packages: `pandas`, `http.client`, `dotenv`, `tqdm`, `pickle`, `logging`, `argparse`, `os`, `time`, `json`

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install required packages using pip:
   ```bash
   pip install pandas tqdm python-dotenv
   ```

3. Clone the repository or download the script to your local machine.

## Configuration
Before running the script, you need to set up an environment file (`scrape-it.env`) with your API key for Google Maps scraping:

```
API_KEY=<your_api_key_here>
```

Place this file in the `creds` directory or specify another directory using the `--scrape_env_dir` argument.

## Usage
Run the script from the command line, specifying the required parameters. Here are the available command-line arguments:

- `--zone`: The geographic zone for scraping (default: 'zarate').
- `--coords`: The coordinates around which to scrape (default: '@-34.106385,-59.082982,13z').
- `--query`: The keyword for scraping (default: 'maderera').
- `--country`: The country code for scraping (default: 'BR').
- `--domain`: The domain for scraping (default: 'com').
- `--start`: The starting index for scraping (default: 0).
- `--end`: The ending index for scraping (default: 1).
- `--output_file`: The name of the final output file (default: 'deduplicated_results.xlsx').
- `--output_dir`: The directory to store output files (default: None, uses current directory).
- `--scrape_env_dir`: The directory containing the `scrape-it.env` file (default: 'creds').

Example command:
```
python google_maps_scraper.py --zone "NewYork" --coords "@40.7128,-74.0060,13z" --query "restaurant" -start 0 --end 10
```


This command will scrape restaurant data in the New York area.

## Output
The script generates several types of output files:

- JSON files for each scraping iteration.
- Pickle files for each scraping iteration.
- Excel files for each scraping iteration and a final consolidated file with deduplicated results.

These files are saved in the specified `output_dir` or in the current directory if none is specified.

## Logging
The script logs its progress and any important information or errors to the console. This can be used for monitoring the scraping process and debugging.

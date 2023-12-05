import json
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from main import GoogleMapsScraper, parse_arguments


@pytest.fixture
def scraper_args():
    return parse_arguments()

@pytest.fixture
def scraper(scraper_args):
    return GoogleMapsScraper(scraper_args)

def test_scrape_data(scraper):
    with patch('main.http.client.HTTPSConnection') as mock_http_conn:
        # Mock the API response as before
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"scrapingResult": {'locals': []}}).encode('utf-8')
        mock_response.status = 200
        mock_http_conn.return_value.getresponse.return_value = mock_response

        scraper.scrape_data()

        assert mock_http_conn.called
        assert mock_response.read.called
        assert len(scraper.current_df_dict) == 1

def test_aggregate_results(scraper):
    with patch('main.os.walk') as mock_os_walk, \
         patch('main.open', new_callable=unittest.mock.mock_open, read_data='data') as mock_open, \
         patch('main.pickle.load') as mock_pickle_load:

        mock_os_walk.return_value = [('/path/to/dicts', ['subdir'], ['file1.pkl', 'file2.pkl'])]
        mock_pickle_load.return_value = {'key': 'value'}

        result = scraper.aggregate_results()

        assert mock_os_walk.called
        assert mock_open.called
        assert isinstance(result, dict)

def test_save_final_results(scraper):
    with patch('main.pd.DataFrame.to_excel') as mock_to_excel:
        scraper.joined_dict = {'key': pd.DataFrame()}

        scraper.save_final_results()

        mock_to_excel.assert_called_once()

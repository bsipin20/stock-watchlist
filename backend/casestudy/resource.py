import random
import urllib.parse
import logging
import string
import requests
import json
import time
from abc import ABCMeta, abstractmethod
class BaseStockClient:
    HEADER = None
    def __init__(self, base_resource, api_key, max_retries=1, retry_delay = 10):
        self.base_resource = base_resource
        self.api_key = api_key
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _make_request(self, endpoint, params=None):
        url = f"{self.base_resource}/{endpoint}"
        headers = {}
        if self.HEADER:
            headers = {self.HEADER: self.api_key}
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise exception for 4xx and 5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    @abstractmethod
    def get_all_stocks(self):
        """
        Method to get all stock prices.
        This method must be implemented by concrete classes.
        """
        raise NotImplementedError

    @abstractmethod
    def get_stock_prices_by_tickers(self, tickers):
        """
        Method to get stock prices for specific tickers.
        This method must be implemented by concrete classes.
        """
        raise NotImplementedError

class TestAlbertStockClient(BaseStockClient):
    STOCKS = {
            "AAPL": 'Apple',
            "MSFT": 'Microsoft',
            "AMZN": 'Amazon',
            "BUD": 'Berkshire Hathaway'
        }

    def get_all_stocks(self):
        return self.STOCKS

    def get_stock_prices_by_tickers(self, tickers):
        result = {}
        for i in self.STOCKS:
            if i in tickers:
                result[i] = random.uniform(1,200)
        logging.info(f'result: {result}')
        return result

class AlbertStockClient(BaseStockClient):
    HEADER = "Albert-Case-Study-API-Key"

    def get_all_stocks(self):
        retries = 0
        while retries < self.max_retries:
            result = self._make_request('casestudy/stock/tickers/')
            if result is not None:
                return result
            retries += 1
            time.sleep(self.retry_delay)
        print("Max retries exceeded. Unable to get all stock prices.")
        return None

    def get_stock_prices_by_tickers(self, tickers):
        retries = 0
        ticker_string = ','.join(tickers)
        while retries < self.max_retries:
            result = self._make_request('casestudy/stock/prices', {'tickers': ticker_string})
            if result is not None:
                return result
            retries += 1
            time.sleep(self.retry_delay)
        print("Max retries exceeded. Unable to get stock prices by tickers.")
        return None

def get_stock_client(resource_uri, api_key, environment):
    if environment == 'development':
        return AlbertStockClient(resource_uri, api_key)
    elif environment == 'local':
        return TestAlbertStockClient("test", "test_key")

if __name__ == "__main__":
    client = get_stock_client("https://app.albert.com", "d2db5753-33f6-4e25-b915-6cbdda7953e7", 'development')
    result = client.get_stock_prices_by_tickers(['AAPL', 'AMZN'])
    print(result)

import random
import logging
import string
import requests
import json
import time

from abc import ABCMeta, abstractmethod

class BaseStockClient:
    def __init__(self, base_resource, max_retries=3, retry_delay = 1):
        self.base_resource = base_resource
        self.max_retries = retry_delay

    def _make_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for 4xx and 5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    @abstractmethod
    def get_all_stocks(self):
        """
        Method to get all stock prices.
        This method must be implemented by derived classes.
        """
        raise NotImplementedError

    @abstractmethod
    def get_stock_prices_by_tickers(self, tickers):
        """
        Method to get stock prices for specific tickers.
        This method must be implemented by derived classes.
        """
        raise NotImplementedError

class TestAlbertStockClient(BaseStockClient):
    STOCKS = {
            "AAPL": 'Apple',
            "GOOG": 'Alphabet', # 'GOOGL
            "MSFT": 'Microsoft',
            "AMZN": 'Amazon',
            "BRK.A": 'Berkshire Hathaway'
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
    BASE_URL = "https://albert-stocks-api.herokuapp.com"

    def get_all_stocks(self):
        retries = 0
        while retries < self.max_retries:
            result = self._make_request('stock/prices')
            if result is not None:
                return result
            retries += 1
            time.sleep(self.retry_delay)
        print("Max retries exceeded. Unable to get all stock prices.")
        return None

    def get_stock_prices_by_tickers(self, tickers):
        retries = 0
        while retries < self.max_retries:
            result = self._make_request('stock/prices', {'tickers': tickers})
            if result is not None:
                return result
            retries += 1
            time.sleep(self.retry_delay)
        print("Max retries exceeded. Unable to get stock prices by tickers.")
        return None


def get_stock_client():
    return TestAlbertStockClient("test")

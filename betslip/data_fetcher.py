# data_fetcher.py
from abc import ABC, abstractmethod
import requests
from requests.exceptions import HTTPError
from datetime import datetime
from . import utils
import numpy as np
import json
import logging
import pandas as pd

class DataFetcher(ABC):
    def __init__(self, config_file_path: str):
        self.config_file_path: str = config_file_path
        self.config: json = json.load(open(config_file_path))

    @abstractmethod
    def fetch_data(self, symbol: str, begin: str, period: str):
        """
        Fetch data for a given symbol, start date, and period.

        :param symbol: Stock symbol to fetch the data for.
        :param begin: Start date for the data in 'YYYY-MM-DD HH:MM:SS' format.
        :param period: Period of the stock data to fetch.
        """
        pass

class XueqiuFetcher(DataFetcher):
    def fetch_data(self, symbol: str, begin: str, period: str) -> pd.DataFrame:
        """
        Fetch data from Xueqiu for a given symbol, start date, and period.

        :param symbol: Stock symbol to fetch the data for.
        :param begin: Start date for the data in 'YYYY-MM-DD HH:MM:SS' format.
        :param period: Period of the stock data to fetch.
        :return: Pandas DataFrame with the stock data.
        """
        max_count_per_request = 142
        total_data = pd.DataFrame()
        current_begin: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_returned_data = pd.DataFrame()
        unchanged_iterations = 0

        while unchanged_iterations < 3:
            begin_timestamp = datetime.strptime(begin, "%Y-%m-%d %H:%M:%S").timestamp()
            json_data = self.get_stock_data(symbol=symbol, begin=current_begin,
                                            count=-max_count_per_request*2 if total_data.empty else -max_count_per_request,
                                            period=period)

            dataframe_data: pd.DataFrame = utils.convert_to_dataframe(json_data) if json_data is not None else pd.DataFrame()

            if dataframe_data.equals(last_returned_data):
                logging.info("No new data fetched")
                unchanged_iterations += 1
                dataframe_data = pd.DataFrame()
            else:
                unchanged_iterations = 0  # Reset the counter if there were changes
                last_returned_data = dataframe_data
                logging.info(f"New data fetched: {dataframe_data.iloc[0]['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} to {dataframe_data.iloc[-1]['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")

            # Concatenate the new data with the previously fetched data
            if not dataframe_data.empty:
                total_data = pd.concat([dataframe_data, total_data]).drop_duplicates().reset_index(drop=True)

            # Check if the earliest entry's date is before the 'begin' parameter
            if not total_data.empty:
                earliest_entry_date: str = total_data.iloc[0]['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                earliest_entry_timestamp = datetime.strptime(earliest_entry_date, "%Y-%m-%d %H:%M:%S").timestamp()

                if earliest_entry_timestamp <= begin_timestamp:
                    break

                # Update current_begin to the earliest date from the data fetched
                current_begin = earliest_entry_date

        return total_data


    def get_stock_data(self, symbol: str, begin: str, period: str, count: int):
        base_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
            "Connection": "keep-alive",
            "Cookie": self.config['Cookie'], 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",  
            "Host": "stock.xueqiu.com",
            "Origin": "https://xueqiu.com",
            "Referer": "https://xueqiu.com/S/{}".format(symbol),
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site"
        }
        params = {
            "symbol": symbol,
            "begin": utils.convert_datetime_to_timestamp(begin),
            "period": period,
            "type": "before",
            "count": count
        }

        try:
            response = requests.get(base_url, headers=headers, params=params)
            logging.info(f'Sending HTTP request with symbol: {symbol}, begin: {begin}, period: {period}, count: {count}')
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')
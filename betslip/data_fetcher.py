# data_fetcher.py
from abc import ABC, abstractmethod
import requests
from requests.exceptions import HTTPError
from datetime import datetime
from . import utils
import numpy as np

class DataFetcher(ABC):
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
    def fetch_data(self, symbol: str, begin: str, period: str):
        """
        Fetch data from Xueqiu for a given symbol, start date, and period.

        :param symbol: Stock symbol to fetch the data for.
        :param begin: Start date for the data in 'YYYY-MM-DD HH:MM:SS' format.
        :param period: Period of the stock data to fetch.
        """
        # Implementation for fetching data from Xueqiu
        # This will involve making an HTTP request to the Xueqiu API and handling the response.
        
        max_count_per_request = 142
        total_data = None
        current_begin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_returned_data = None
        unchanged_iterations = 0

        while True and unchanged_iterations < 3:
            

            # Convert 'begin' to a timestamp
            begin_timestamp = datetime.strptime(begin, "%Y-%m-%d %H:%M:%S").timestamp()

            # Call the get_stock_data function
            json_data = self.get_stock_data(symbol=symbol, begin=current_begin, count=-max_count_per_request*2 if total_data is None else -max_count_per_request, period=period)

            # Convert the JSON response to a NumPy array
            numpy_data = utils.convert_to_numpy(json_data) if json_data is not None else None

            if np.array_equal(numpy_data, last_returned_data):
                unchanged_iterations += 1
                continue
            else:
                unchanged_iterations = 0  # Reset the counter if there were changes
                last_returned_data = numpy_data

            # Concatenate the new data with the previously fetched data
            if total_data is None and numpy_data is not None:
                total_data = numpy_data
            elif numpy_data is not None:
                total_data = np.concatenate((numpy_data, total_data), axis=0)
            # If numpy_data is None, total_data remains unchanged, so no else clause is needed

            print(f'total_data: {total_data}')

            # Check if the earliest entry's date is before the 'begin' parameter
            earliest_entry_date = total_data[0][0]
            earliest_entry_timestamp = datetime.strptime(earliest_entry_date, "%Y-%m-%d %H:%M:%S").timestamp()

            if earliest_entry_timestamp <= begin_timestamp:
                break

            # Update current_begin to the earliest date from the data fetched
            current_begin = earliest_entry_date

            

        # Now 'total_data' contains all the fetched data up to the 'begin' date
        return total_data

    def get_stock_data(self, symbol: str, begin: str, period: str, count: int):
        print(f'symbol: {symbol}, begin: {begin}, period: {period}, count: {count}')
        base_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
            "Connection": "keep-alive",
            "Cookie": "cookiesu=221699801989558; Hm_lvt_1db88642e346389874251b5a1eded6e3=1699801990; device_id=99404e292d34ac332240f7f2681a989c; s=ce1wg9129g; xq_a_token=ea87bbc526aeba1634ca35d18b897613124a1e24; xqat=ea87bbc526aeba1634ca35d18b897613124a1e24; xq_r_token=1eb0a76bd89369c707971fbd3e769211fb151904; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjQ1NjYxOTMyNTQsImlzcyI6InVjIiwiZXhwIjoxNzAyMzk0MTg4LCJjdG0iOjE2OTk4MDIxODgzOTksImNpZCI6ImQ5ZDBuNEFadXAifQ.imuNy9X7XupJ5AXJHtwJKiVzpZ_MtvVy4i5sb9bdOe2Id9ae7CYzoHhbfexy20NGHiA3X88XduZbzh5qoGtDz4RRoqxZi9lv2-dSO4WfJc1Z6GmiP7Ud3L-BvBVI8fwmfmKHmangoUlIhKRu-UwHVqkgXkOREuyBBklTpnsTKRjDxWaimLpe44ROlmP9BCS7XGz0IhuCh6BZS6TUCFfGBCsIZjk7OBB_wAqadC1vxXIHG3p_j6EzatI9NG_mMMq9qVjnMki6IuE0PaoM025mz1b_H9il0v1pceRyijE6VKb9aBWN25vIgypOw8Dudrbt5NQmp6rlwwDF1vluTDPdBw; xq_is_login=1; u=4566193254; snbim_minify=true; is_overseas=1; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1699802309", 
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
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')
# cli.py
import argparse
from betslip.file_handler import save_to_npy, save_to_pkl, save_to_csv

from betslip.data_fetcher import XueqiuFetcher
from betslip.utils import DEFAULT_CONFIG_PATH, PERIODS
import logging

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

    parser = argparse.ArgumentParser(description='Fetch and save stock quote data.')
    parser.add_argument('-src', '--source', help='Data source', default='xueqiu')
    parser.add_argument('-symbol', help='Stock symbol', required=True)
    parser.add_argument('-period', help='Period of the stock data: day/week/month/quarter/year/120m/60m/30m/15m/5m/1m', default='day')
    parser.add_argument('-begin', help='Start date for the data', required=True)
    parser.add_argument('-config', help='Path to the config file', default=DEFAULT_CONFIG_PATH)
    parser.add_argument('-save_fmt', nargs='+', help='Format to save the data in: npy/pkl/csv', default=['pkl'])

    args = parser.parse_args()

    logging.info(f"Start fetching data with symbol: {args.symbol}, begin: {args.begin}, period: {args.period}, source: {args.source}, save_fmt: {args.save_fmt}")

    # Choose the appropriate fetcher based on the source argument
    if args.source.lower() == 'xueqiu':
        fetcher = XueqiuFetcher(config_file_path=args.config)
    else:
        # Placeholder for future fetcher implementations
        raise ValueError(f"Unsupported source: {args.source}")

    if args.period not in PERIODS:
        raise ValueError(f"Unsupported period: {args.period}")

    # Fetch data using the selected fetcher
    data = fetcher.fetch_data(symbol=args.symbol, begin=args.begin, period=args.period)
    logging.info(f"Data fetched:\n {data}")

    filename = f"{args.symbol}-{args.period}"

    # Save the data to the appropriate format
    for fmt in args.save_fmt:
        if fmt.lower() == 'npy':
            save_to_npy(data, filename)
        elif fmt.lower() == 'pkl':
            save_to_pkl(data, filename)
        elif fmt.lower() == 'csv':
            save_to_csv(data, filename)
        else:
            raise ValueError(f"Unsupported save format: {fmt}")

if __name__ == '__main__':
    main()

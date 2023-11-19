# cli.py
import argparse
from betslip.file_handler import save_to_npy

# Assuming you have a fetcher for Xueqiu in data_fetcher.py like this:
from betslip.data_fetcher import XueqiuFetcher

def main():
    parser = argparse.ArgumentParser(description='Fetch and save stock quote data.')
    parser.add_argument('-src', '--source', help='Data source', default='xueqiu')
    parser.add_argument('-symbol', help='Stock symbol', required=True)
    parser.add_argument('-period', help='Period of the stock data', default='day')
    parser.add_argument('-begin', help='Start date for the data', required=True)

    args = parser.parse_args()

    print(f"Symbol: {args.symbol}")
    print(f"Begin: {args.begin}")
    print(f"Period: {args.period}")

    # Choose the appropriate fetcher based on the source argument
    if args.source.lower() == 'xueqiu':
        fetcher = XueqiuFetcher()
    else:
        # Placeholder for future fetcher implementations
        raise ValueError(f"Unsupported source: {args.source}")

    # Fetch data using the selected fetcher
    data = fetcher.fetch_data(symbol=args.symbol, begin=args.begin, period=args.period)

    print(f"Data: {data}")
    
    # Save to .npy file
    filename = f"{args.symbol}-{args.period}.npy"
    save_to_npy(data, filename)

if __name__ == '__main__':
    main()

import os
import sys
import time
from pathlib import Path
from pyserum.connection import conn
from pyserum.market import Market
from config import SERUM_MARKETS

cc = conn("https://api.mainnet-beta.solana.com/")

def main():
    for i in SERUM_MARKETS:
        data = get_orderbook_data(SERUM_MARKETS[i])
        unix_time, ask_price, bid_price = data[0], data[1], data[2]
        write_data(i, unix_time, ask_price, bid_price)

def get_orderbook_data(srm_market_address):
    market = Market.load(cc, srm_market_address)
    asks = market.load_asks()
    bids = market.load_bids()
    unix_time = time.time()

    for i in asks:
        market_asks = i[5]
        ask_price = market_asks[0]
        break

    for i in bids:
        market_bids = i[5]
        bid_price = market_bids[0]

    return unix_time, ask_price, bid_price

def write_data(market, unix_time, bid_price, ask_price):
    file_name = sys.argv[0].replace('.py', '')
    folder_path = f'data/{file_name}/'
    header_string = 'time,bid_price,ask_price\n'
    string_to_write = f'{unix_time},{bid_price},{ask_price}\n'

    print(f"Writing {market} data...")
    if os.path.exists(folder_path):
        with open(f"{folder_path}{market}.csv", 'a') as f:
            f.write(string_to_write)
    else:
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        with open(f"{folder_path}{market}.csv", 'w') as f:
            f.write(f"{header_string}{string_to_write}")

if __name__ == '__main__':
    main()

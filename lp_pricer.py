import os
import sys
import time
import requests
from pathlib import Path
from config import LP_ADDRESSES

def main():
    for i in LP_ADDRESSES:
        print(i)
        contract_address = LP_ADDRESSES[i][-1]
        json = http_request(contract_address)
        lp_price = lp_pricer(json, i)

        unix_time, x_price, y_price = lp_price[0], lp_price[1], lp_price[2]
        write_data(sys.argv[0].replace('.py', ''), i, unix_time, x_price, y_price)

def http_request(contract_address):
    print(contract_address)
    url = f'https://public-api.solscan.io/account/tokens?account={contract_address}'
    req = requests.get(url)
    json = req.json()

    return json

def lp_pricer(json, token_pair):
    unix_time = time.time()
    for i in json:
        if i['tokenAddress'] == LP_ADDRESSES[token_pair][0]:
            x = i['tokenAmount']['uiAmount']

        if i['tokenAddress'] == LP_ADDRESSES[token_pair][1]:
            y = i['tokenAmount']['uiAmount']

    x_price = x / y
    y_price = y / x

    return unix_time, x_price, y_price

def write_data(file_name, trade_pair, unix_time, x_price, y_price):
    folder_path = f'data/{file_name}/'
    header_string = 'time,x_pair,y_pair\n'
    string_to_write = f'{unix_time},{x_price},{y_price}\n'

    if os.path.exists(folder_path):
        with open(f'{folder_path}{trade_pair}.csv', 'a') as f:
            f.write(string_to_write)
    else:
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        with open(f'{folder_path}{trade_pair}', 'w') as f:
            f.write(f'{header_string}{string_to_write}')

if __name__ == '__main__':
    main()

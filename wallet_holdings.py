import os
import sys
import time
from pathlib import Path
import requests
from config import WALLETS
from time import sleep

def main():
    for i in WALLETS:
        json = http_request(i)
        get_holdings(json, i)
        sleep(1)

def http_request(wallet_address):
    url = f'https://public-api.solscan.io/account/tokens?account={wallet_address}'
    req = requests.get(url)
    json = req.json()

    return json

def get_holdings(json, wallet_address):
    unix_time = time.time()
    print(f'Writing holdings data for {wallet_address}')
    for i in json:
        token_address = i['tokenAddress']
        token_name = i['tokenName']
        token_amount = i['tokenAmount']['uiAmountString']

        if token_name == '':
            token_name = 'N/A'

        string_to_write = f'{unix_time},{token_address},{token_name},{token_amount}\n'
        write_data(sys.argv[0].replace('.py', ''), wallet_address, string_to_write)

def write_data(file_name, wallet_address, string_to_write):
    folder_path = f'data/{file_name}/'
    header_string = 'time,token_address,token_name,token_amount\n'

    if os.path.exists(folder_path):
        with open(f'{folder_path}{wallet_address}.csv', 'a') as f:
            f.write(string_to_write)
    else:
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        with open(f'{folder_path}{file_name}', 'w') as f:
            f.write(f'{header_string}{string_to_write}')

if __name__ == '__main__':
    main()

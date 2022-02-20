import os
import sys
import time
from pathlib import Path
import requests
from config import TOKENS
from time import sleep

def main():
    for i in TOKENS:
        holders_json = http_request(TOKENS[i])
        top_100_holdings = sum_top_100_holders(holders_json)
        write_data(sys.argv[0].replace(".py", ""), i, top_100_holdings)
        sleep(1)

def http_request(token_address):
    url = f"https://public-api.solscan.io/token/holders?tokenAddress={token_address}&offset=0&limit=100"
    req = requests.get(url)
    json = req.json()
    data = json['data']

    return data

def sum_top_100_holders(json):
    tokens_held = []
    for i in json:
        decimals = i['decimals']
        amount_held = i['amount']

        insert_decimal_list = []
        for k in str(amount_held):
            insert_decimal_list.append(k)

        #Index at which to insert decimal point at
        insert_decimal_at_index = len(insert_decimal_list) - decimals
        insert_decimal_list.insert(insert_decimal_at_index, '.')

        balances = float(list_to_string(insert_decimal_list))
        tokens_held.append(balances)

    total_amount_held = sum(tokens_held)
    return total_amount_held

def write_data(file_name, token_name, sum_amount):
    folder_path = f"data/{file_name}/" #Path to write data
    token_file_name = f"{token_name}.csv"
    header_string = "time,sum\n"
    string_to_write = f"{time.time()},{sum_amount}\n"

    print(f"Writing {token_name} data...")
    if os.path.exists(folder_path):
        with open(f"{folder_path}{token_file_name}", 'a') as f:
            f.write(string_to_write)
    else:
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        with open(f"{folder_path}{token_file_name}", 'w') as f:
            f.write(f"{header_string}{string_to_write}")

def list_to_string(list_with_strings): #Takes list of strings and converts them to a string
    empty_string = ''

    for element in list_with_strings:
        empty_string += element

    return empty_string

if __name__ == '__main__':
    main()

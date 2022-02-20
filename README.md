# solana-data

Variety of scripts and utilities created for collecting on-chain data for Solana 

Script names mostly self-explanatory. ```wallet_holdings.py``` scrapes all the SPL Tokens a wallet is holding. ```top_holders.py``` sums the amount held by top 100 wallets. ```serum_price.py``` returns bid and ask for a given Serum market. ```lp_pricer.py``` returns the price for a given liquidity pool contract addresss. ```main.py``` runs each script one after another.

## Installation and Use

To install required libraries run ```pip install -r requirements.txt```

To use add your chosen wallets, contract addresses, and Serum markets in ```config.py```.

# Fyyx Wallet Finder

Fyyx Wallet Finder is a Python application built with PyQt5 that searches for cryptocurrency wallets with a non-zero balance and saves the mnemonic seeds of the found wallets.

## Features

- Search for wallets with a balance in Bitcoin (BTC) and Ethereum (ETH).
- Generates new wallets using BIP39 mnemonic seeds.
- Provides a user-friendly graphical interface.
- Logs search results and errors to a log file.
- Saves mnemonic seeds of wallets with balances.

## Installation

### Requirements

- Python 3.x
- PyQt5
- bip_utils
- requests
- dotenv

Install the required Python packages using pip:

```bash
pip install PyQt5 bip-utils requests python-dotenv


INSTALL:

- git clone https://github.com/your_username/fyyx-wallet-finder.git
- cd fyyx-wallet-finder
- python Finder.py

(Enter your Etherscan API key when prompted.)

Click on the "Search Wallet" button to start searching for wallets.

Once the search is complete, check the wallets_with_balance_secrets.txt file in the project directory for mnemonic seeds of wallets with balances.



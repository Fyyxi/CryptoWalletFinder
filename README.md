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

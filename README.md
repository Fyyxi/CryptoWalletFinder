# Fyyx Wallet Finder

## Overview

Fyyx Wallet Finder is a tool that searches for Bitcoin and Ethereum wallets with a balance. It uses BIP39 mnemonic phrases to generate wallets and checks their balances using the Etherscan API for Ethereum and Blockchain.info for Bitcoin. The tool includes a graphical user interface (GUI) built with PyQt5.

## Features

- Generates BIP39 mnemonic phrases.
- Derives Bitcoin and Ethereum addresses from the mnemonic phrases.
- Checks the balance of the generated addresses.
- Logs the results and saves wallets with a balance to files.
- Provides a GUI for easy interaction.

## Installation

### Prerequisites

- Python 3.7 or later
- `pip` (Python package installer)

### Step-by-Step Guide

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/fyyx-wallet-finder.git
    cd fyyx-wallet-finder
    ```

2. **Install the Required Packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application:**

    ```bash
    python Finder.py
    ```

## Usage

1. **Start the Application:**

    After running `python Finder.py`, the Fyyx Wallet Finder GUI will appear.

2. **Begin Wallet Search:**

    - Click on the "Search Wallet" button to start searching for wallets.
    - The tool will generate mnemonic phrases, derive wallet addresses, and check their balances.
    - Results will be displayed in the GUI and logged to the log file.

3. **Stop the Search:**

    - Click the "Stop Searching" button to stop the search process.

4. **Review Results:**

    - Wallets with a balance will be saved to `wallets_with_balance.txt` and their corresponding seeds to `wallets_with_balance_secrets.txt`.

## Logging

- Logs are stored in the `fyyx_wallet_finder.log` file.
- The log includes information about generated seeds, wallet addresses, balances, and any errors encountered during the search process.

## Dependencies

- `requests`
- `PyQt5`
- `bip-utils`
- `python-dotenv`

These dependencies are listed in the `requirements.txt` file and can be installed using `pip`.

Feel free to contribute by submitting pull requests to improve the tool. Happy wallet hunting!

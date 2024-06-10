import sys
import os
import time
import logging
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
    Bip39WordsNum,
)
from dotenv import load_dotenv

# Constants
LOG_FILE_NAME = "fyyx_wallet_finder.log"
WALLETS_FILE_NAME = "wallets_with_balance.txt"
SECRETS_FILE_NAME = "wallets_with_balance_secrets.txt"

# Get the absolute path of the directory where the script is located
directory = os.path.dirname(os.path.abspath(__file__))
# Initialize directory paths
log_file_path = os.path.join(directory, LOG_FILE_NAME)
wallets_file_path = os.path.join(directory, WALLETS_FILE_NAME)
secrets_file_path = os.path.join(directory, SECRETS_FILE_NAME)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),  # Log to a file
        logging.StreamHandler(sys.stdout),  # Log to standard output
    ],
)

class WalletFinderThread(QThread):
    search_finished = pyqtSignal(str)
    wallets_checked = pyqtSignal(int)

    def __init__(self, wallets_file_path, secrets_file_path, etherscan_api_key):
        super().__init__()
        self.wallets_file_path = wallets_file_path
        self.secrets_file_path = secrets_file_path
        self.etherscan_api_key = etherscan_api_key
        self.stopped = False  # Flag to indicate if the search is stopped

    def run(self):
        wallets_checked = 0
        while not self.stopped:
            try:
                seed = bip()  # Generate a new seed for each iteration
                BTC_address = bip44_BTC_seed_to_address(seed)
                BTC_balance = check_BTC_balance(BTC_address)

                logging.info(f"Seed: {seed}")
                logging.info(f"BTC address: {BTC_address}")
                logging.info(f"BTC balance: {BTC_balance} BTC")
                logging.info("")

                ETH_address = bip44_ETH_wallet_from_seed(seed)
                ETH_balance = check_ETH_balance(ETH_address, self.etherscan_api_key)

                logging.info(f"ETH address: {ETH_address}")
                logging.info(f"ETH balance: {ETH_balance} ETH")

                if BTC_balance > 0 or ETH_balance > 0:
                    logging.info("(!) Wallet with balance found!")
                    result = "Wallet with balance found! Seed: {}".format(seed)
                    with open(self.wallets_file_path, "a") as f:
                        f.write(seed + "\n")
                    with open(self.secrets_file_path, "a") as f:
                        f.write(seed + "\n")
                else:
                    result = "No wallet with balance found."

                wallets_checked += 1
                self.wallets_checked.emit(wallets_checked)
                self.search_finished.emit(result)

                time.sleep(1)  # Add some delay before checking the next seed
            except Exception as e:
                result = "Error occurred during wallet search: {}".format(str(e))
                self.search_finished.emit(result)

    def stop(self):
        self.stopped = True


class FyyxWalletFinder(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fyyx Wallet Finder")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Apply glassy style
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 150);
                color: black;
                border: 1px solid rgba(255, 255, 255, 200);
                border-radius: 10px;
            }
            QPushButton {
                background: rgba(0, 0, 0, 100);
                color: white;
                border: 1px solid rgba(255, 255, 255, 200);
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 150);
            }
            QLabel {
                background: transparent;
                padding: 5px;
            }
        """)

        # Title label
        self.title_label = QLabel("Fyyx Wallet Finder")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Search button
        self.search_button = QPushButton("Search Wallet")
        self.search_button.clicked.connect(self.start_search)

        # Search result label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)

        # Wallets checked label
        self.wallets_checked_label = QLabel("Wallets Checked: 0")
        self.wallets_checked_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title_label)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.wallets_checked_label)

        self.setLayout(layout)

        self.searching = False  # Flag to indicate if searching is in progress
        self.thread = None  # Thread instance to hold the search thread

    def start_search(self):
        if not self.searching:
            self.searching = True
            self.search_button.setText("Stop Searching")
            self.result_label.setText("Searching...")
            self.thread = WalletFinderThread(wallets_file_path, secrets_file_path, os.getenv("ETHERSCAN_API_KEY"))
            self.thread.search_finished.connect(self.update_result)
            self.thread.wallets_checked.connect(self.update_wallets_checked)
            self.thread.start()
        else:
            self.searching = False
            if self.thread:
                self.thread.stop()
            self.search_button.setText("Search Wallet")
            self.result_label.setText("Search stopped.")

    def update_result(self, result):
        if result.startswith("Error"):
            # Display error only once
            self.result_label.setText(result)
        else:
            # Display only if it's a new wallet found
            if self.result_label.text() != result:
                self.result_label.setText(result)

    def update_wallets_checked(self, count):
        self.wallets_checked_label.setText(f"Wallets Checked: {count}")


def bip():
    # Generate a 12-word BIP39 mnemonic
    return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)


def bip44_ETH_wallet_from_seed(seed):
    # Generate an Ethereum wallet from a BIP39 seed.

    # Generate the seed from the mnemonic
    seed_bytes = Bip39SeedGenerator(seed).Generate()

    # Create a Bip44 object for Ethereum derivation
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)

    # Derive the account 0, change 0, address_index 0 path (m/44'/60'/0'/0/0)
    bip44_acc_ctx = (
        bip44_mst_ctx.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
    )

    # Get the Ethereum address
    return bip44_acc_ctx.PublicKey().ToAddress()


def bip44_BTC_seed_to_address(seed):
    # Generate the seed from the mnemonic
    seed_bytes = Bip39SeedGenerator(seed).Generate()

    # Generate the Bip44 object
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)

    # Generate the Bip44 address (account 0, change 0, address 0)
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
    bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
    bip44_addr_ctx = bip44_chg_ctx.AddressIndex(0)

    # Print the address
    return bip44_addr_ctx.PublicKey().ToAddress()


def check_ETH_balance(address, etherscan_api_key, retries=3, delay=5):
    # Etherscan API endpoint to check the balance of an address
    api_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={etherscan_api_key}"

    for attempt in range(retries):
        try:
            # Make a request to the Etherscan API
            response = requests.get(api_url)
            data = response.json()

            # Check if the request was successful
            if data["status"] == "1":
                # Convert Wei to Ether (1 Ether = 10^18 Wei)
                balance = int(data["result"]) / 1e18
                return balance
            else:
                logging.error("Error getting balance: %s", data["message"])
                return 0
        except Exception as e:
            if attempt < retries - 1:
                logging.error(
                    f"Error checking balance, retrying in {delay} seconds: {str(e)}"
                )
                time.sleep(delay)
            else:
                logging.error("Error checking balance: %s", str(e))
                return 0


def check_BTC_balance(address, retries=3, delay=5):
    # Check the balance of the address
    for attempt in range(retries):
        try:
            response = requests.get(f"https://blockchain.info/balance?active={address}")
            data = response.json()
            balance = data[address]["final_balance"]
            return balance / 100000000  # Convert satoshi to bitcoin
        except Exception as e:
            if attempt < retries - 1:
                logging.error(
                    f"Error checking balance, retrying in {delay} seconds: {str(e)}"
                )
                time.sleep(delay)
            else:
                logging.error("Error checking balance: %s", str(e))


def main():
    # Load environment variables
    load_dotenv()

    # Check if the ETHERSCAN_API_KEY is set
    etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")

    if not etherscan_api_key:
        logging.warning("ETHERSCAN_API_KEY environment variable is not set.")
        etherscan_api_key = input("Enter your Etherscan API key: ")
        os.environ["ETHERSCAN_API_KEY"] = etherscan_api_key

    app = QApplication(sys.argv)

    # Initialize and show the Fyyx Wallet Finder UI
    finder = FyyxWalletFinder()
    finder.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

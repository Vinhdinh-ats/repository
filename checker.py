import time
import random
# from checker import WalletChecker

class WalletChecker:
    def __init__(self, log_callback, stats_callback):
        self.log = log_callback
        self.stats = stats_callback
        self.running = False
        self.selected_chains = []

        self.checked = 0
        self.total_found = 0.0

    def set_chains(self, chains):
        self.selected_chains = chains

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            mnemonic = self.generate_mnemonic()
            balance = self.check_balance(mnemonic)
            log_line = f"Wallet Check: {mnemonic} | Balance: {balance}"
            self.log(log_line)
            self.checked += 1
            self.total_found += float(balance)
            self.stats(self.checked, self.total_found)
            time.sleep(0.1)

    def generate_mnemonic(self): 
        from utils import generate_mnemonic
        return generate_mnemonic()

    def check_balance(self, mnemonic):
        return "0"

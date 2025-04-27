import random
import os
import sys

def load_word_list(filename="wordlist.txt"):
    """Read list from file and return as list."""
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        file_path = os.path.join(base_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found at {file_path}")
        return []  # Trả về danh sách rỗng nếu file không tồn tại

def generate_mnemonic(word_count=12):
    """Generate random mnemonic strings."""
    word_list = load_word_list()
    return " ".join(random.choices(word_list, k=word_count))

def format_balance(balance):
    """Format balances in standard currency."""
    try:
        value = float(balance)
        return f"${value:,.2f}"
    except ValueError:
        return "$0.00"

def is_valid_chain(chain):
    """Check if the chain name is valid."""
    return chain in {"BTC", "ETH", "BNB", "USDT", "LTC", "SOL"}
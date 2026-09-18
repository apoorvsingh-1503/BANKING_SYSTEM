from datetime import datetime
from cryptography import encrypt_data, decrypt_data
from configuration import File_Transaction
import os
def transaction_log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    encrypted_entry = encrypt_data(log_entry)
    with open(File_Transaction, "a") as f:
        f.write(encrypted_entry + "\n")

def show_transaction_history():
    if os.path.exists(File_Transaction):
        print("\n--- Transaction History ---")
        with open(File_Transaction, "r") as f:
            for line in f:
                if line.strip():
                    print(decrypt_data(line.strip()))
    else:
        print("No history found.")

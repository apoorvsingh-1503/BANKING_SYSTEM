from cryptography.fernet import Fernet
import os
from configuration import Key_File

def load_or_create_key():
    if not os.path.exists(Key_File):
        key = Fernet.generate_key()
        with open(Key_File, "wb") as key_file:
            key_file.write(key)
    else:
        with open(Key_File, "rb") as key_file:
            key = key_file.read()
    return key

cipher = Fernet(load_or_create_key())

def encrypt_data(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(token: str) -> str:
    try:
        return cipher.decrypt(token.encode()).decode()
    except Exception:
        return ""
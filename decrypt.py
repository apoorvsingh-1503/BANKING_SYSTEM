from cryptography.fernet import Fernet

# 1. Load the secret key
with open("secret.key", "rb") as key_file:
    key = key_file.read()
cipher = Fernet(key)

# 2. Read the encrypted file (Change filename as needed)
filename = "data_account.enc"
with open(filename, "rb") as enc_file:
    data = enc_file.read()

filename = "data_transaction.enc"
with open(filename, "rb") as enc_file:
    encrypted_data = enc_file.read()

# 3. Decrypt and display the content
try:
    ddata = cipher.decrypt(data).decode()
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    print("\n--- Decrypted Content ---")
    print(ddata)
    print(decrypted_data)
except Exception as e:
    print("Decryption failed. Ensure your 'secret.key' matches the key used for encryption.")

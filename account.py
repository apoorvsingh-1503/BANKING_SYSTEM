import os
import random
import string
from datetime import datetime
from cryptography import encrypt_data, decrypt_data
from configuration import File_Account, File_Transaction
from transaction import transaction_log   # or keep initial log here

def acc_generator():
    return "".join(random.choices(string.digits, k=10))

def hs_pin_generator():
    return "".join(random.choices(string.digits, k=4))

def file_delete():
    from configuration import File_Beneficiary, Key_File
    for file in [File_Transaction, File_Account, File_Beneficiary, Key_File]:
        if os.path.exists(file):
            os.remove(file)
    print("ALL LOGS AND ENCRYPTION KEYS DELETED")

def account_creation():
    if os.path.exists(File_Account):
            print("Account Already Exists")
            ch = input("Do you want to continue (1) or Create a new account (2)? ")
            if ch == "2":
                file_delete()
            else: 
                return
    
    name = input("ENTER ACCOUNT HOLDER NAME : ")
    account_no = acc_generator()
    pin = input("CREATE 4 DIGIT STANDARD PIN : ")
    
    q1 = "NAME OF FAVOURITE MOVIE"
    q2 = "NAME OF BIRTH CITY"
    q3 = "FAVOURITE COLOUR"
    
    print("GIVE ANSWERS TO 3 SECURITY QUESTIONS:")
    a1 = input(f"{q1} : ")
    a2 = input(f"{q2} : ")
    a3 = input(f"{q3} : ")
    
    hs_pin = hs_pin_generator()
    print(f"YOUR HIGH SECURITY PIN IS : {hs_pin} (KEEP IT SAFELY)")
    twpin = input("Create a TWPIN (Transfer/Withdrawal PIN): ")
    balance_initial = 2500.0

    raw_data = f"{name}\n{account_no}\n{pin}\n{q1}:{a1}\n{q2}:{a2}\n{q3}:{a3}\n{hs_pin}\n{twpin}\n{balance_initial}\n"
    
    with open(File_Account, "w") as f:
        f.write(encrypt_data(raw_data))

    with open(File_Transaction, "w") as f:
        initial_log = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Account Created.\n"
        f.write(encrypt_data(initial_log) + "\n")
        
    print(f"Account created successfully! Your Account Number is {account_no}")
def load_account_data():
    if not os.path.exists(File_Account):
        return None

    with open(File_Account, "r") as f:
        encrypted_content = f.read()

    decrypted_content = decrypt_data(encrypted_content)
    lines = [line.strip() for line in decrypted_content.split("\n") if line.strip()]

    if len(lines) < 9:
        return None

    data = {}
    data["name"] = lines[0]
    data["acc_no"] = lines[1]
    data["pin"] = lines[2]

    data["q1"], data["a1"] = lines[3].split(":")
    data["q2"], data["a2"] = lines[4].split(":")
    data["q3"], data["a3"] = lines[5].split(":")

    data["hs_pin"] = lines[6]
    data["t_pin"] = lines[7]
    data["balance"] = float(lines[8])
    return data

def update_account_balance(new_balance):
    data = load_account_data()
    
    if data:
        raw_data = (
            f"{data['name']}\n"
            f"{data['acc_no']}\n"
            f"{data['pin']}\n"
            f"{data['q1']}:{data['a1']}\n"
            f"{data['q2']}:{data['a2']}\n"
            f"{data['q3']}:{data['a3']}\n"
            f"{data['hs_pin']}\n"
            f"{data['t_pin']}\n"
            f"{new_balance}\n")
    
    with open(File_Account, "w") as f:
        f.write(encrypt_data(raw_data))
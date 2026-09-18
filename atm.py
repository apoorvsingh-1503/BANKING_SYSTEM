from cryptography.fernet import Fernet
from datetime import datetime
import os
import random

# FILES 
File_Account = "data_account.enc"
File_Transaction = "data_transaction.enc"
File_Beneficiary = "data_beneficiary.enc"
Key_File = "secret.key"

def load_or_create_key():
    """Loads the encryption key or generates a new one if it doesn't exist."""
    if not os.path.exists(Key_File):
        key = Fernet.generate_key()
        with open(Key_File, "wb") as key_file:
            key_file.write(key)
    else:
        with open(Key_File, "rb") as key_file:
            key = key_file.read()
    return key

# Initialize Fernet cipher
cipher = Fernet(load_or_create_key())

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(token):
    try:
        return cipher.decrypt(token.encode()).decode()
    except Exception:
        return ""

def acc_generator():
    return "".join(random.choices(string.digits, k=10))

def hs_pin_generator():
    return "".join(random.choices(string.digits, k=10))

def transaction_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    encrypted_entry = encrypt_data(log_entry)
    with open(File_Transaction, "a") as f:
        f.write(encrypted_entry + "\n")

def file_delete():
    for file in [File_Transaction, File_Account, File_Beneficiary, Key_File]:
        if os.path.exists(file):
            os.remove(file)
    print("ALL LOGS AND ENCRYPTION KEYS DELETED")

def add_beneficiary_to_file():
    b_name = input("Beneficiary Name: ")
    b_acc = input("Beneficiary A/c Number: ")
    b_limit = input("Max Transfer Limit: ")
    plain_text = f"{b_name},{b_acc},{b_limit}\n"
    encrypted_text = encrypt_data(plain_text)
    with open(File_Beneficiary, "a") as f:
        f.write(encrypted_text + "\n")
    print("Beneficiary added successfully.")

def print_beneficiary_file():
    if not os.path.exists(File_Beneficiary):
        print("No beneficiaries found.")
        return
    print("\n--- Beneficiary List ---")
    with open(File_Beneficiary, "r") as f:
        for idx, line in enumerate(f, 1):
            decrypted_line = decrypt_data(line.strip())
            if decrypted_line:
                name, acct, limit = decrypted_line.strip().split(",")
                print(f"{idx}. Name: {name} | A/c: {acct} | Limit: {limit}")

def delete_beneficiary_from_file():
    if not os.path.exists(File_Beneficiary):
        print("No beneficiaries file found.")
        return

    with open(File_Beneficiary, "r") as f:
        lines = f.readlines()
    
    beneficiaries = [decrypt_data(l.strip()) for l in lines if l.strip()]
    
    if not beneficiaries:
        print("No beneficiaries to delete.")
        return

    for idx, b in enumerate(beneficiaries, 1):
        name, acct, *_ = b.strip().split(",")
        print(f"{idx}. {name} ({acct})")
        
    choice = input("Enter serial number to delete: ")
    del_idx = int(choice) - 1

    if 0 <= del_idx < len(beneficiaries):
        beneficiaries.pop(del_idx)
        with open(File_Beneficiary, "w") as f:
            for b in beneficiaries:
                f.write(encrypt_data(b if b.endswith('\n') else b + '\n') + "\n")
        print("Beneficiary deleted.")
    else:
        print("Invalid selection.")

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
            f"{new_balance}\n"
        )

        with open(File_Account, "w") as f:
            f.write(encrypt_data(raw_data))

def login():
    data = load_account_data()
    if not data:
        print("CREATE AN ACCOUNT TO CONTINUE")
        return False
    a = 3
    while a >= 3:
        epin = input("ENTER YOUR STANDARD PIN : ")
        if epin == data["pin"]:
            print("LOGIN SUCCESSFUL!")
            dashboard(data)
            return True
        else:
            a -= 1
            print(f"INCORRECT PIN. ATTEMPTS LEFT = {a}")
    print("\nTOO MANY FAILED ATTEMPTS. SECURITY SYSTEM TRIGGERED")
    ehs_pin = input("ENTER YOUR HIGH SECURITY PIN : ")
    if ehs_pin == data["hs_pin"]:
        print("SECURITY VERIFICATION PASSED")
        dashboard(data)
        return True
    else:
        ans1 = input(f"Answer Q1 ({data['q1']}): ")
        ans2 = input(f"Answer Q2 ({data['q2']}): ")
        ans3 = input(f"Answer Q3 ({data['q3']}): ")
        if ans1 == data["a1"] and ans2 == data["a2"] and ans3 == data["a3"]:
            print("SECURITY VERIFICATION PASSED")
            dashboard(data)
            return True
        else:
            print("SECURITY VERIFICATION FAILED ! DELETING ALL LOGS")
            file_delete()
            return False

def dashboard(data):
    while True:
        print("\n--- Banking Menu ---")
        print("1. Add Beneficiary")
        print("2. Get All Beneficiary Data")
        print("3. Transfer Money")
        print("4. Withdraw Money")
        print("5. Check Total Balance")
        print("6. Get Transaction History")
        print("7. Change PIN")
        print("8. Delete Beneficiary")
        print("9. Logout")
        c = int(input("Select an option (1-9): "))
        if c == 1:
            hs = input("ENTER HIGH SECURITY PIN : ")
            if hs == data["hs_pin"]:
                add_beneficiary_to_file()
            else:
                print("INCORRECT HIGH SECURITY PIN ENTERED")
        elif c == 2:
            print_beneficiary_file()
        elif c in [3, 4]:
            amount = float(input("Enter amount: "))
            current_data = load_account_data()
            if amount > current_data["balance"]:
                print("TRANSACTION CANNOT BE PROCESSED. INSUFFICIENT BALANCE")
            else:
                tp = input("Enter TPIN: ")
                if tp == current_data["t_pin"]:
                    new_bal = current_data["balance"] - amount
                    update_account_balance(new_bal)
                    action = "Transferred" if c == 3 else "Withdrawn"
                    transaction_log(f"{action} amount: {amount}. New Balance: {new_bal}")
                    print(f"Transaction successful! New Balance: {new_bal}")
                else:
                    print("Incorrect TPIN.")
        elif c == 5:
            current_data = load_account_data()
            print(f"Total Balance: {current_data['balance']}")
        elif c == 6:
            if os.path.exists(File_Transaction):
                print("\n--- Transaction History ---")
                with open(File_Transaction, "r") as f:
                    for line in f:
                        if line.strip():
                            print(decrypt_data(line.strip()))
            else:
                print("No history found.")
        elif c == 7:
            ans1 = input(f"Answer Q1 ({data['q1']}): ")
            ans2 = input(f"Answer Q2 ({data['q2']}): ")
            ans3 = input(f"Answer Q3 ({data['q3']}): ")
            entered_hs = input("Enter High-Security PIN: ")
            if ans1 == data["a1"] and ans2 == data["a2"] and ans3 == data["a3"] and entered_hs == data["hs_pin"]:
                new_pin = input("Enter new standard PIN: ")
                data["pin"] = new_pin
                update_account_balance(data["balance"])
                print("PIN changed successfully.")
            else:
                print("Verification failed.")
        elif c == 8:
            tp = input("Enter TPIN: ")
            hs = input("Enter High-Security PIN: ")
            if tp == data["t_pin"] and hs == data["hs_pin"]:
                delete_beneficiary_from_file()
            else:
                print("Incorrect credentials.")
        elif c == 9:
            break

def main():
    while True:
        print(f"=== WELCOME TO APOORV BANKING SYSTEM ===")
        print("(a) Already having an account")
        print("(b) Create an account")
        choice = input("Select option (a/b or 'q' to quit): ").lower()
        
        if choice == 'b':
            account_creation()
        elif choice == 'a':
            login()
        elif choice == 'q':
            break

if __name__ == "__main__":
    main()

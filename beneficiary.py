import os
from cryptography import encrypt_data, decrypt_data
from configuration import File_Beneficiary
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

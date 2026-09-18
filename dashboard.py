import os  # Added just in case, though show_transaction_history handles it
from account import load_account_data, update_account_balance
from beneficiary import (
    add_beneficiary_to_file,
    print_beneficiary_file,
    delete_beneficiary_from_file
)
from transaction import transaction_log, show_transaction_history

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
        
        try:
            c = int(input("Select an option (1-9): "))
        except ValueError:
            print("Please enter a valid number between 1 and 9.")
            continue

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
            # Fixed: Utilize the imported function instead of undefined variables
            show_transaction_history()
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

from account import load_account_data, file_delete
from dashboard import dashboard

def login():
    data = load_account_data()
    if not data:
        print("CREATE AN ACCOUNT TO CONTINUE")
        return False
    a = 3
    while a >0:
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
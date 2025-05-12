#....................................... account number ...................................
import random
#........................................ crate DATE And Time ...............................
from datetime import datetime
#......................................... file check .....................................
import os
#......................................... password hide ...................................
import hashlib

#.................................. Dictionary to store account details ......................................
accounts = {}
admin_password_hash = hashlib.sha256("admin123".encode()).hexdigest()

#..................... Generate random 4-digit account number ...........................................
def generate_account_number():
    return random.randint(1000, 9999)

#..................................... Function to hash a password using SHA-256 ....................
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#..................................... Admin login .................................................
def admin_login():
    print("\n--- Admin Login ---")
    password = input("Enter admin password: ")
    hashed_password = hash_password(password)
    
    if hashed_password == admin_password_hash:
        print("👍 Admin Login successfully.")
        return True
    else:
        print("❌ Incorrect admin password.")
        return False

#............................................. Create account .............................................
def create_account():
    if not admin_login():
        return

    account_number = generate_account_number()
    while account_number in accounts:
        account_number = generate_account_number()

    name = input("Enter account holder's name: ")
    nic = input("Enter account holder's NIC: ")
    telephone = input("Enter account holder's telephone number: ")

    while True:
        try:
            initial_balance = float(input("Enter initial balance: "))
            if initial_balance < 0:
                print("Initial balance cannot be negative. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number for the balance.")

    password = input("Create a password for the new account: ")
    hashed_password = hash_password(password)
    creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    accounts[account_number] = {
        'holder_name': name,
        'nic': nic,
        'telephone': telephone,
        'balance': initial_balance,
        'transactions': [f"{creation_time} - Account created with balance {initial_balance}"],
        'password': hashed_password,
        'creation_time': creation_time
    }

    print(f"✅ Account created successfully! Account Number: {account_number}")
    print(f"⏰ Account creation time: {creation_time}")
    save_accounts_to_file()

    with open("account.txt", "a") as f:
        f.write(f"{creation_time} - Account {account_number} created for {name}, NIC: {nic}, Tel: {telephone}, Balance: {initial_balance}\n")

#.................................................. View all accounts .............................................
def view_all_accounts():
    if not admin_login():
        return

    if not accounts:
        print("❌ No accounts found.")
        return

    print("\n--- All Accounts ---")
    for acc_no, acc in accounts.items():
        print(f"Account Number: {acc_no}")
        print(f"Name         : {acc['holder_name']}")
        print(f"NIC          : {acc['nic']}")
        print(f"Telephone    : {acc['telephone']}")
        print(f"Balance      : {acc['balance']}")
        print(f"Created On   : {acc['creation_time']}")
        print("-" * 30)

#...................................................... View all transactions ....................................
def view_all_transactions():
    if not admin_login():
        return

    if not accounts:
        print("❌ No transactions to display.")
        return

    print("\n--- All Transactions ---")
    for acc_no, acc in accounts.items():
        print(f"Account Number: {acc_no} - {acc['holder_name']}")
        for tx in acc['transactions']:
            print(f"  {tx}")
        print("-" * 30)

#................................................... Save accounts to file ....................................
def save_accounts_to_file():
    with open("account.txt", "w") as file:
        for account_number, account in accounts.items():
            file.write(f"{account_number}: {account['holder_name']}, {account['nic']}, {account['telephone']}, {account['balance']}, {account['creation_time']}, {account['password']}\n")
            for transaction in account['transactions']:
                file.write(f"  - {transaction}\n")

#............................................... Load accounts from file ..........................................
def load_accounts_from_file():
    if os.path.exists("account.txt"):
        try:
            with open("account.txt", "r") as file:
                lines = file.readlines()
                current_account = None

                for line in lines:
                    line = line.strip()
                    if line.startswith("  -"):
                        if current_account:
                            current_account['transactions'].append(line.strip())
                    else:
                        parts = line.split(": ")
                        if len(parts) == 2:
                            account_info = parts[1].split(", ")
                            account_number = int(parts[0])
                            holder_name = account_info[0]
                            nic = account_info[1]
                            telephone = account_info[2]
                            balance = float(account_info[3])
                            creation_time = account_info[4]
                            password = account_info[5]
                            current_account = {
                                'holder_name': holder_name,
                                'nic': nic,
                                'telephone': telephone,
                                'balance': balance,
                                'transactions': [],
                                'password': password,
                                'creation_time': creation_time
                            }
                            accounts[account_number] = current_account
        except Exception as e:
            print(f"❌ Error loading file: {e}")
    else:
        print("📂 No previous account data found.")

#.................................................... Deposit money .......................................
def deposit_money():
    try:
        account_number = int(input("Enter account number: "))
        if account_number not in accounts:
            print("❌ Account number does not exist.")
            return

        password = input("Enter your password: ")
        hashed_password = hash_password(password)
        if hashed_password != accounts[account_number]['password']:
            print("❌ Incorrect password.")
            return

        while True:
            try:
                amount = float(input("Enter amount to deposit: "))
                if amount <= 0:
                    print("❌ Amount must be positive.")
                else:
                    break
            except ValueError:
                print("❌ Invalid amount.")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        accounts[account_number]['balance'] += amount
        accounts[account_number]['transactions'].append(f"{timestamp} - Deposited {amount}")
        print(f"💰 Deposited {amount}. New balance: {accounts[account_number]['balance']}")
        save_accounts_to_file()

        with open("deposit money.txt", "a") as f:
            f.write(f"{timestamp} - Account {account_number} deposited {amount}. New balance: {accounts[account_number]['balance']}\n")
    except ValueError:
        print("❌ Invalid account number.")

#...................................................... Withdraw money ................................
def withdraw_money():
    try:
        account_number = int(input("Enter account number: "))
        if account_number not in accounts:
            print("❌ Account number does not exist.")
            return

        password = input("Enter your password: ")
        hashed_password = hash_password(password)
        if hashed_password != accounts[account_number]['password']:
            print("❌ Incorrect password.")
            return

        while True:
            try:
                amount = float(input("Enter amount to withdraw: "))
                if amount <= 0:
                    print("❌ Amount must be positive.")
                elif amount > accounts[account_number]['balance']:
                    print("❌ Insufficient funds.")
                else:
                    break
            except ValueError:
                print("❌ Invalid amount.")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        accounts[account_number]['balance'] -= amount
        accounts[account_number]['transactions'].append(f"{timestamp} - Withdrew {amount}")
        print(f"💵 Withdrew {amount}. New balance: {accounts[account_number]['balance']}")
        save_accounts_to_file()

        with open("withdraw money.txt", "a") as f:
            f.write(f"{timestamp} - Account {account_number} withdrew {amount}. New balance: {accounts[account_number]['balance']}\n")
    except ValueError:
        print("❌ Invalid account number.")

#................................................. Check balance .........................................
def check_balance():
    try:
        account_number = int(input("Enter account number: "))
        if account_number not in accounts:
            print("❌ Account number does not exist.")
            return

        password = input("Enter your password: ")
        hashed_password = hash_password(password)
        if hashed_password != accounts[account_number]['password']:
            print("❌ Incorrect password.")
            return

        balance = accounts[account_number]['balance']
        print(f"💳 Balance: {balance}")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("check balance.txt", "a") as f:
            f.write(f"{timestamp} - Account {account_number} checked balance: {balance}\n")
    except ValueError:
        print("❌ Invalid account number.")

#................................................ Transaction history .......................................
def transaction_history():
    try:
        account_number = int(input("Enter account number: "))
        if account_number not in accounts:
            print("❌ Account number does not exist.")
            return

        password = input("Enter your password: ")
        hashed_password = hash_password(password)
        if hashed_password != accounts[account_number]['password']:
            print("❌ Incorrect password.")
            return

        print(f"📜 Transactions for account {account_number}:")
        for tx in accounts[account_number]['transactions']:
            print(f"  {tx}")
    except ValueError:
        print("❌ Invalid account number.")

#.................................................... Transfer money .....................................
def transfer_money():
    try:
        from_acc = int(input("Enter your account number: "))
        if from_acc not in accounts:
            print("❌ Sender account does not exist.")
            return

        password = input("Enter your password: ")
        hashed_password = hash_password(password)
        if hashed_password != accounts[from_acc]['password']:
            print("❌ Incorrect password.")
            return

        to_acc = int(input("Enter recipient account number: "))
        if to_acc not in accounts:
            print("❌ Recipient account does not exist.")
            return

        amount = float(input("Enter amount to transfer: "))
        if amount <= 0:
            print("❌ Amount must be greater than zero.")
            return
        if amount > accounts[from_acc]['balance']:
            print("❌ Insufficient balance.")
            return

        # Perform transfer
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        accounts[from_acc]['balance'] -= amount
        accounts[to_acc]['balance'] += amount

        accounts[from_acc]['transactions'].append(f"{timestamp} - Transferred {amount} to account {to_acc}")
        accounts[to_acc]['transactions'].append(f"{timestamp} - Received {amount} from account {from_acc}")

        print(f"✅ Transfer of {amount} from account {from_acc} to {to_acc} completed.")
        save_accounts_to_file()

        with open("transfer money.txt", "a") as f:
            f.write(f"{timestamp} - Transfer from {from_acc} to {to_acc} of amount {amount}\n")

    except ValueError:
        print("❌ Invalid input.")

#.......................................... Admin menu ............................................
def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Create Account")
        print("2. View All Accounts")
        print("3. View All Transactions")
        print("4. Exit")
        choice = input("Please select an option (1-4): ")

        if choice == '1':
            create_account()
        elif choice == '2':
            view_all_accounts()
        elif choice == '3':
            view_all_transactions()
        elif choice == '4':
            break
        else:
            print("❌ Invalid choice.")

#....................................... User menu .....................................
def user_menu():
    while True:
        print("\n--- User Menu ---")
        print("1. Deposit Money 💰")
        print("2. Withdraw Money 💵")
        print("3. Check Balance 💳")
        print("4. Transaction History 📜")
        print("5. Transfer Money 💸")
        print("6. Exit 🚪")
        choice = input("Please select an option (1-6): ")

        if choice == '1':
            deposit_money()
        elif choice == '2':
            withdraw_money()
        elif choice == '3':
            check_balance()
        elif choice == '4':
            transaction_history()
        elif choice == '5':
            transfer_money()
        elif choice == '6':
            break
        else:
            print("❌ Invalid choice.")

#................................... Main menu ........................................
def main_menu():
    load_accounts_from_file()
    while True:
        print("\n--- Main Menu ---")
        print("1. Admin Account 🧑‍💼")
        print("2. User Account 👤")
        print("3. Exit 🚪")
        choice = input("Please select an option (1-3): ")

        if choice == '1':
            admin_menu()
        elif choice == '2':
            user_menu()
        elif choice == '3':
            print("🙏 Thank you for using this banking system!")
            break
        else:
            print("❌ Invalid choice.")

#........................................ Start program .....................................
if __name__ == "__main__":
    main_menu()

import datetime
import random
import hashlib
class Account:
    def __init__(self, username, password, name, acc_type, pin):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()  # Secure password storage
        self.pin = hashlib.sha256(pin.encode()).hexdigest()  # Secure PIN storage
        self.name = name
        self.acc_number = random.randint(1000000000, 9999999999)
        self.acc_type = acc_type
        self.balance = 0.0
        self.transactions = []
        self.loan_balance = 0.0
        print(f"Account created successfully!\nName: {self.name}\nAccount No: {self.acc_number}\nType: {self.acc_type}\n")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append((datetime.datetime.now(), "Deposit", amount, self.balance))
            print(f"Deposited {amount}. Current balance: {self.balance}")
        else:
            print("Invalid deposit amount!")

    def withdraw(self, amount, pin):
        if hashlib.sha256(pin.encode()).hexdigest() == self.pin:
            if 0 < amount <= self.balance:
                self.balance -= amount
                self.transactions.append((datetime.datetime.now(), "Withdrawal", amount, self.balance))
                print(f"Withdrawn {amount}. Remaining balance: {self.balance}")
            else:
                print("Insufficient balance or invalid amount!")
        else:
            print("Incorrect PIN!")

    def transfer(self, receiver, amount, pin):
        if hashlib.sha256(pin.encode()).hexdigest() == self.pin:
            if 0 < amount <= self.balance:
                self.balance -= amount
                receiver.balance += amount
                self.transactions.append((datetime.datetime.now(), "Transfer to", amount, self.balance))
                receiver.transactions.append((datetime.datetime.now(), "Transfer from", amount, receiver.balance))
                print(f"Transferred {amount} to {receiver.name}. Your new balance: {self.balance}")
            else:
                print("Insufficient funds or invalid amount!")
        else:
            print("Incorrect PIN!")

    def display_transactions(self):
        print(f"\nTransaction History for {self.name} (Acc: {self.acc_number})")
        for trans in self.transactions:
            print(f"{trans[0]} - {trans[1]}: {trans[2]} - Balance: {trans[3]}")

    def check_balance(self):
        print(f"Current balance for {self.name}: {self.balance}")

    def apply_interest(self):
        if self.acc_type == "Savings":
            interest = self.balance * 0.04  # 4% annual interest
            self.balance += interest
            self.transactions.append((datetime.datetime.now(), "Interest Added", interest, self.balance))
            print(f"Interest of {interest} applied. New balance: {self.balance}")

    def take_loan(self, amount):
        if amount > 0:
            self.loan_balance += amount
            self.balance += amount
            self.transactions.append((datetime.datetime.now(), "Loan Taken", amount, self.balance))
            print(f"Loan of {amount} approved. Your new balance: {self.balance}")
        else:
            print("Invalid loan amount!")

class Bank:
    def __init__(self):
        self.accounts = {}
        self.admin_password = "admin123"
        self.logged_in_user = None

    def create_account(self, username, password, name, acc_type, pin):
        if username in self.accounts:
            print("Username already exists! Choose a different one.")
            return None
        if acc_type not in ["Savings", "Current"]:
            print("Invalid account type! Choose Savings or Current.")
            return None
        account = Account(username, password, name, acc_type, pin)
        self.accounts[username] = account
        return account

    def login(self, username, password):
        account = self.accounts.get(username, None)
        if account and account.password == hashlib.sha256(password.encode()).hexdigest():
            self.logged_in_user = account
            print(f"Welcome, {account.name}! You are now logged in.")
        else:
            print("Invalid username or password!")

    def logout(self):
        if self.logged_in_user:
            print(f"Goodbye, {self.logged_in_user.name}!")
            self.logged_in_user = None
        else:
            print("No user is logged in.")

    def admin_panel(self, password):
        if password == self.admin_password:
            print("\nAdmin Panel - Account Overview:")
            for acc in self.accounts.values():
                print(f"Account: {acc.acc_number} | Name: {acc.name} | Type: {acc.acc_type} | Balance: {acc.balance} | Loan: {acc.loan_balance}")
        else:
            print("Incorrect admin password!")

# Example Usage
if __name__ == "__main__":
    bank = Bank()
    while True:
        print("\n1. Create Account\n2. Login\n3. Deposit\n4. Withdraw\n5. Transfer\n6. Check Balance\n7. View Transactions\n8. Apply Interest\n9. Take Loan\n10. Logout\n11. Admin Panel\n12. Exit")
        choice = input("Enter choice: ")
        
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            pin = input("Set a 4-digit PIN: ")
            name = input("Enter full name: ")
            acc_type = input("Enter account type (Savings/Current): ")
            bank.create_account(username, password, name, acc_type, pin)
        
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            bank.login(username, password)
        
        elif choice == "3" and bank.logged_in_user:
            amount = float(input("Enter deposit amount: "))
            bank.logged_in_user.deposit(amount)
        
        elif choice == "4" and bank.logged_in_user:
            amount = float(input("Enter withdrawal amount: "))
            pin = input("Enter your PIN: ")
            bank.logged_in_user.withdraw(amount, pin)
        
        elif choice == "5" and bank.logged_in_user:
            receiver_username = input("Enter recipient username: ")
            receiver = bank.accounts.get(receiver_username, None)
            if receiver:
                amount = float(input("Enter amount to transfer: "))
                pin = input("Enter your PIN: ")
                bank.logged_in_user.transfer(receiver, amount, pin)
            else:
                print("Recipient not found!")
        
        elif choice == "10":
            bank.logout()
        
        elif choice == "12":
            print("Exiting... Thank you for banking with us!")
            break
        else:
            print("Invalid choice or login required!")

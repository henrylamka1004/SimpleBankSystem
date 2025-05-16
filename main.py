from client import Client
from banking import Bank

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

bank = Bank()
width = 50
print("*" * width)
print(f"{' Welcome to Bank System ':*^{width}}")
print("*" * width)

running1 = True
running2 = True

while running1:
    print("Choose an option:\n1. Open new bank account\n2. Open existing account\n3. Exit")
    try:
        choice1 = int(input("1, 2 or 3: ") or 3)
    except:
        running1 = False

    if choice1 == 1:
        print("\n==============\nCreate a new bank account with a name and starting balance.\nPlease fill in the account name and starting deposit amount below:\n==============\n")
        while True:
            acc_name = input("Account Name: ").strip()
            if acc_name == '':
                print("\n==============\nWrong name format! Please enter again\n==============\n")
                continue
            break
        
        while True:
            try:
                init_deposit = float(input("Deposit amount: "))
                break
            except ValueError:
                print("\n==============\nWrong deposit format! Please enter again\n==============\n")
            except:
                running1 = False
                break
        
        bank.create_account(acc_name, init_deposit)
        
    elif choice1 == 2:
        print("\n==============\nTo access your account, please enter your credentials below:\n==============\n")
        acc_name = input("Account Name: ").strip()
        acc_no = input("Account Number: ").strip()
        if bank.auth(acc_name, acc_no) is False:
            pass
        else:
            client = Client(acc_no)
            while running2:
                print("\n==============\nChoose an option:\n1. Deposit to accounts\n2. Withdraw from accounts\n3. Transfer money to other accounts\n4. Exit\n==============\n")
                choice2 = int(input("1, 2, 3 or 4: ") or 4)
                if choice2 == 1:
                    while True:
                        try:
                            amount = float(input("amount: "))
                            amount = float(f"{amount:.2f}")
                            if amount <= 0:
                                print("\n==============\nAmount must larger than 0. Please enter again\n==============\n")
                                continue
                            break
                        except ValueError:
                            print("\n==============\nWrong amount format! Please enter again\n==============\n")
                        except:
                            running2 = False
                            break
                            
                    client.deposit(amount, client.account_no)
                    
                elif choice2 == 2:
                    while True:
                        try:
                            amount = float(input("amount: "))
                            amount = float(f"{amount:.2f}")
                            if amount <= 0:
                                print("\n==============\nAmount must larger than 0. Please enter again\n==============\n")
                                continue
                            break
                        except ValueError:
                            print("\n==============\nWrong amount format! Please enter again\n==============\n")
                        except:
                            running2 = False
                            break
                            
                    client.withdraw(amount, client.account_no)
                    
                elif choice2 == 3:
                    while True:
                        try:
                            amount = float(input("amount: "))
                            amount = float(f"{amount:.2f}")
                            if amount <= 0:
                                print("\n==============\nAmount must larger than 0. Please enter again\n==============\n")
                                continue
                            break
                        except ValueError:
                            print("\n==============\nWrong amount format! Please enter again\n==============\n")
                        except:
                            running2 = False
                            break
                    rcv_acc_no = input("Transfer to Account Number: ").strip()
                    client.transfer_money(rcv_acc_no, amount)
                else:
                    running2 = False
    
    else:
        running1 = False

print("\n==============\nGoodBye!\n==============\n")


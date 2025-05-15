from banking import Bank
from model import DataBase, Transaction

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class Client:
    bank = Bank()
    def __init__(self, acc_no):
        self.account_no = acc_no

    def transfer_money(self, rcv_acc_no, amount, success="Y"):
        transcation = Transaction(self.account_no, rcv_acc_no, amount)
        current_dt, current_time = self.bank.refresh_datetime()
        transcation.current_dt, transcation.current_time = current_dt, current_time
        txn_record = {
            "pay_account_no": [transcation.pay_accno],
            "receive_account_no": [transcation.rcv_accno],
            "amount": [transcation.amount],
            "txn_date": [transcation.current_dt],
            "txn_time": [transcation.current_time],
        }
        
        # check rcv account exists
        if len(self.bank.check_csv(DataBase.account_db, f"account_no == {rcv_acc_no}")) == 0:
            print("\n==============\nCannot find recieve account\n==============\n")
            txn_record["success"] = "N"
            self.bank.append_csv(DataBase.transaction_db, txn_record)
            return
            
        if self.withdraw(amount, self.account_no) is False:
            txn_record["success"] = "N"
            self.bank.append_csv(DataBase.transaction_db, txn_record)
            return
            
        self.deposit(amount, rcv_acc_no)
        txn_record["success"] = "Y"
        self.bank.append_csv(DataBase.transaction_db, txn_record)
        print("\n==============\nTransfer amount to another account\n==============\n")
        
    def deposit(self, amount, acc_no):
        acc_no = int(acc_no)
        acc_bal = self.bank.check_csv(DataBase.balance_db, f"account_no == {acc_no}")["balance"].reset_index(drop=True)[0]
        acc_bal += amount
        acc_bal = round(acc_bal,2)
        df_bal = self.bank.read_csv(DataBase.balance_db)
        df_bal.loc[df_bal["account_no"] == acc_no, "balance"] = acc_bal
        current_dt, current_time = self.bank.refresh_datetime()
        df_bal.loc[df_bal["account_no"] == acc_no, "update_date"] = current_dt
        df_bal.loc[df_bal["account_no"] == acc_no, "update_time"] = current_time
        self.bank.to_csv(df_bal, DataBase.balance_db)
        print(f"\n==============\nNew Balance: {acc_bal}\n==============\n")
        
    def withdraw(self, amount, acc_no):
        acc_no = int(acc_no)
        acc_bal = self.bank.check_csv(DataBase.balance_db, f"account_no == {acc_no}")["balance"].reset_index(drop=True)[0]
        if acc_bal < amount:
            print("\n==============\nNot enough balance\n==============\n")
            return False
        acc_bal = acc_bal - amount
        acc_bal = round(acc_bal,2)
        df_bal = self.bank.read_csv(DataBase.balance_db)
        df_bal.loc[df_bal["account_no"] == acc_no, "balance"] = acc_bal
        current_dt, current_time = self.bank.refresh_datetime()
        df_bal.loc[df_bal["account_no"] == acc_no, "update_date"] = current_dt
        df_bal.loc[df_bal["account_no"] == acc_no, "update_time"] = current_time
        self.bank.to_csv(df_bal, DataBase.balance_db)
        print(f"\n==============\nRemain Balance: {acc_bal}\n==============\n")
    
    
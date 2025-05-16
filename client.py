from banking import Bank
from model import DataBase

class Client:
    bank = Bank()
    def __init__(self, acc_no):
        self.account_no = acc_no

    def transfer_money(self, rcv_acc, amount, success="Y"):
        
        txn_record = self.bank.get_transaction_info(self.account_no, rcv_acc, amount)
        
        # check rcv account exists
        if len(self.bank.check_csv(DataBase.account_db, f"account_no == {rcv_acc}")) == 0:
            print("\n==============\nCannot find recieve account\n==============\n")
            txn_record["success"] = "N"
            self.bank.append_csv(DataBase.transaction_db, txn_record)
            return
            
        if self.withdraw(amount, self.account_no) is False:
            txn_record["success"] = "N"
            self.bank.append_csv(DataBase.transaction_db, txn_record)
            return
            
        self.deposit(amount, rcv_acc)
        txn_record["success"] = "Y"
        self.bank.append_csv(DataBase.transaction_db, txn_record)
        print("\n==============\nTransfer amount to another account\n==============\n")
        
    def deposit(self, amount, acc_no):
        acc_no = int(acc_no)
        acc_bal = self.bank.check_csv(DataBase.balance_db, f"account_no == {acc_no}")["balance"].reset_index(drop=True)[0]
        
        txn_record = self.bank.get_transaction_info("88888888", self.account_no, amount)
        txn_record["success"] = "Y"
        self.bank.append_csv(DataBase.transaction_db, txn_record)
        
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
        
        txn_record = self.bank.get_transaction_info(self.account_no, "88888888", amount)
        
        if acc_bal < amount:
            print("\n==============\nNot enough balance\n==============\n")
            txn_record["success"] = "N"
            self.bank.append_csv(DataBase.transaction_db, txn_record)
            return False
        txn_record["success"] = "Y"
        self.bank.append_csv(DataBase.transaction_db, txn_record)
        acc_bal = acc_bal - amount
        acc_bal = round(acc_bal,2)
        df_bal = self.bank.read_csv(DataBase.balance_db)
        df_bal.loc[df_bal["account_no"] == acc_no, "balance"] = acc_bal
        current_dt, current_time = self.bank.refresh_datetime()
        df_bal.loc[df_bal["account_no"] == acc_no, "update_date"] = current_dt
        df_bal.loc[df_bal["account_no"] == acc_no, "update_time"] = current_time
        self.bank.to_csv(df_bal, DataBase.balance_db)
        print(f"\n==============\nRemain Balance: {acc_bal}\n==============\n")
    
    
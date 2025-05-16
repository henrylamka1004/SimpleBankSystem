from datetime import datetime
import pandas as pd


from model import DataBase, Account, Balance, Transaction

class Bank:
    
    def __init__(self):
        ...

    def read_csv(self, file):
        return pd.read_csv(file)

    def to_csv(self, df, file):
        df.to_csv(file, index=False)
        
    def append_csv(self, file, record):
        orig_df = pd.read_csv(file)
        new_df = pd.DataFrame.from_dict(record)
        df_merged = pd.concat([orig_df, new_df], ignore_index=True, sort=False)
        df_merged.to_csv(file, index=False)

    def update_csv(self, file, k1, v1, k2, v2):
        df = pd.read_csv(file)
        print(df.dtypes)
        df.loc[df[k1] == v1, k2] = v2
        df.to_csv(file, index=False)
        
    def check_csv(self, file, where_clause):
        df = pd.read_csv(file)
        df = df.query(where_clause)
        return df

    def refresh_datetime(self):
        now = datetime.now()
        current_dt = datetime.strftime(now, "%Y%m%d")
        current_time = datetime.strftime(now, "%H%M%S")
        return current_dt, current_time

    def get_transaction_info(self, pay_acc, rcv_acc, amount):
        transcation = Transaction(pay_acc, rcv_acc, amount)
        current_dt, current_time = self.refresh_datetime()
        transcation.current_dt, transcation.current_time = current_dt, current_time
        txn_record = {
            "pay_account_no": [transcation.pay_accno],
            "receive_account_no": [transcation.rcv_accno],
            "amount": [transcation.amount],
            "txn_date": [transcation.current_dt],
            "txn_time": [transcation.current_time],
        }
        return txn_record
    
    def create_account(self, acc_name, init_deposit):
        if len(self.check_csv(DataBase.account_db, f"account_name == '{acc_name}'")) > 0:
            print("\n==============\nAccount Name exists already.\n==============\n")
            return
        
        account = Account(acc_name)
        current_dt, current_time = self.refresh_datetime()
        account.create_dt, account.create_time = current_dt, current_time

        balance = Balance(account.account_no, init_deposit)
        current_dt, current_time = self.refresh_datetime()
        balance.update_date, balance.update_time = current_dt, current_time
        
        print(f"\n==============\nAccount created successfully. Your account number is {account.account_no}.\n==============\n")

        # insert data
        acc_record = {
            "account_no": [account.account_no],
            "account_name": [account.account_name],
            "active": [account.active],
            "create_dt": [account.create_dt],
            "create_time": [account.create_time],
        }
        self.append_csv(DataBase.account_db, acc_record)

        bal_record = {
            "account_no": [balance.account_no],
            "balance": [balance.balance],
            "update_date": [balance.update_date],
            "update_time": [balance.update_time],
        }
        self.append_csv(DataBase.balance_db, bal_record)

    def auth(self, acc_name, acc_no):
        if len(self.check_csv(DataBase.account_db, f"account_name == '{acc_name}' and account_no == {acc_no}")) > 0:
            print("\n==============\nLogin Successfully\n==============\n")
            return True
        else:
            print("\n==============\nLogin Failed\n==============\n")
            return False
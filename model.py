import uuid
import os

class DataBase:
    account_db = os.path.join(".", "data", "account.csv")
    balance_db = os.path.join(".", "data", "balance.csv")
    transaction_db = os.path.join(".", "data", "transaction.csv")

class Account:
    def __init__(self, acc_name):
        self.account_name = acc_name
        self.account_no = uuid.uuid4().fields[0]
        self.active = "Y"
        
    def __str__(self):
        return f"Account(account_name={self.account_name}, account_no={self.account_no})"
        
class Balance:
    def __init__(self, acc_no, balance):
        self.account_no = acc_no
        self.balance = balance
        
    def __str__(self):
        return f"Balance(account_no={self.account_no}, balance={self.balance})"

class Transaction:
    def __init__(self, pay_accno, rcv_accno, amount):
        self.pay_accno = pay_accno
        self.rcv_accno = rcv_accno
        self.amount = amount
        
    def __str__(self):
        return f"Transaction(pay_accno={self.pay_accno}, rcv_accno={self.rcv_accno}, amount={self.amount})"
import portfolio as pf
import portfolio.transaction as tr
import re
import pandas as pd
import io

class AccountHandler(pf.SettedBaseHandler):
    def __init__(self, *args, **kwargs):
        self._type_dict = { "BANK": BankAccount }
        return super(AccountHandler, self).__init__(*args, **kwargs)

class AccountArray(pf.SettedBaseArray):
    def __init__(self, *args, **kwargs):
        super(AccountArray,self).__init__(array_type_handler = AccountHandler, *args, **kwargs)

class Account(pf.SettedBaseclass):
    _transactions = None
    
    def _parse_setts(self, setts):
        if setts["transactions_file"] is not None:
            self.read_transactions(self._parse_var(setts["transactions_file"]))
        
        return self

    def read_transactions(self, text_file_path):
        self._transactions = tr.TransactionStatement().from_text_file(text_file_path)
        return self
        
    @property
    def transactions(self):
        return self._transactions
    
    
class BankAccount(Account):
    pass
    
 
		
    

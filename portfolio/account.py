import portfolio as pf

class AccountHandler(pf.SettedBaseHandler):
    def __init__(self, *args, **kwargs):
        self._type_dict = { "BANK": BankAccount }
        return super(AccountHandler, self).__init__(*args, **kwargs)

class AccountArray(pf.SettedBaseArray):
    def __init__(self, *args, **kwargs):
        super(AccountArray,self).__init__(array_type_handler = AccountHandler, *args, **kwargs)

class Account(pf.SettedBaseclass):
    pass
    
class BankAccount(Account):
    pass
    
 
		
    

import portfolio as pf
import portfolio.transaction as tr
import re
import pandas as pd
import io
import numpy as np

class AccountHandler(pf.SettedBaseHandler):
    def __init__(self, *args, **kwargs):
        self._type_dict = { "BANK": BankAccount }
        return super(AccountHandler, self).__init__(*args, **kwargs)

class AccountArray(pf.SettedBaseArray):
    def __init__(self, *args, **kwargs):
        super(AccountArray,self).__init__(array_type_handler = AccountHandler, *args, **kwargs)

class Account(pf.SettedBaseclass):
    """
    An account.
    
    Attributes
    ----------
    transactions : TransactionStatement
        Transactions by this account
    
    asset_names : list
        List of all assets held by this account
    
    asset_holdings : pd.DataFrame
        Current (cumulated) asset holdings for this account
        Considers the last status and the transactions since then
    """
    
    _transactions = None
    
    def __init__(self, *args, **kwargs):
        self._default_setts.update({
                                    "transactions_file" : None
                                    })
        return super(Account, self).__init__(*args, **kwargs)
    
    
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
    
    @property
    def asset_names(self):
        assets_status = self._transactions.status.asset_name
        assets_transactions = self._transactions.transactions.asset_name
        return pd.concat((assets_status, assets_transactions)).unique()
        
    def _value_for_asset(self, asset_name):
        """
        Value for the asset with `asset_name` held by the account.
        """
        status = self._transactions.status
        trans = self._transactions.transactions
        
        status = status[status["asset_name"] == asset_name]
        last_status_date = status["date"].max()
        last_status = status[status["date"] == last_status_date]["value"].values[0]
        
        trans = trans[trans["asset_name"] == asset_name]
        trans_after_last_status = trans[trans["date"] > last_status_date]["value"].sum()
        
        return last_status + trans_after_last_status
        
    @property
    def asset_holdings(self):
        anames, values = [], []
        for aname in self.asset_names:
            anames.append(aname)
            values.append(self._value_for_asset(aname))
        return pd.DataFrame({"asset_name" : anames, "value" : values})
        
    
class BankAccount(Account):
    pass
    

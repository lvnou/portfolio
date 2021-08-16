import pandas as pd
import portfolio as pf
import re
import io

class TransactionStatement(pf.BaseClass):
    _status_df = None
    _transactions_df = None
    
    def _parse_df_from_text(self,text):
        cols = {"Asset Name" : "asset_name", "Value": "value", "Date": "date"}
        df = super(TransactionStatement,self)._parse_df_from_text(text, cols=cols)
        
        df["value"] = pd.to_numeric(df["value"], downcast = "float")
        df["date"] = pd.to_datetime(df["date"],dayfirst=True)
        
        return df
    
    def _parse_status_df_from_text(self, text):
        self._status_df = self._parse_df_from_text(text)
        return self
    
    def _parse_transaction_df_from_text(self,text):
        self._transactions_df = self._parse_df_from_text(text)
        return self
    
    def from_text_file(self, text_file_path):
        _status_begin = "# STATUS"
        _status_end = "# END STATUS"
        _transactions_begin = "# TRANSACTIONS"
        _transactions_end = "# END TRANSACTIONS"
        
        def extract_text_between(text, start, end):
            res = re.search("{}(.*){}".format(start, end),text,re.M | re.DOTALL)
            return res.group(1)
            
        cont = open(text_file_path, "r").read()
        status_text = extract_text_between(cont, _status_begin, _status_end)
        transaction_text = extract_text_between(cont, _transactions_begin, _transactions_end)
        self._parse_status_df_from_text(status_text)
        self._parse_transaction_df_from_text(transaction_text)
        
        return self
        
    @property
    def status(self):
        return self._status_df
        
    @property
    def transactions(self):
        return self._transactions_df

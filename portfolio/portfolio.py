import portfolio as pf
import portfolio.account as acc

class PortfolioHandler(pf.SettedBaseHandler):
    def __init__(self, *args, **kwargs):
        self._type_dict = { "PORTFOLIO": Portfolio }
        return super(PortfolioHandler, self).__init__(*args, **kwargs)


class Portfolio(pf.SettedBaseclass):
    _accounts = None
    
    def __init__(self,json_file_path):
        return super(Portfolio,self).__init__(json_file_path)
        
        
    def _parse_setts(self, setts):
        acc_json = self._parse_var(setts["account_json"])
        if acc_json is not None:
            self._accounts = acc.AccountArray(acc_json)
        
        return self
        
    @property
    def accounts(self):
        return self._accounts
        

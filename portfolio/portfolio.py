import portfolio as pf
import portfolio.account as acc
import portfolio.asset as asse

class PortfolioHandler(pf.SettedBaseHandler):
    def __init__(self, *args, **kwargs):
        self._type_dict = { "PORTFOLIO": Portfolio }
        return super(PortfolioHandler, self).__init__(*args, **kwargs)


class Portfolio(pf.SettedBaseclass):
    _accounts = None
    _assets = None
    
    def __init__(self,json_file_path):
        self._default_setts.update({
                                    "account_json" : None,
                                    "asset_json" : None
                                    })
                                
        return super(Portfolio,self).__init__(json_file_path)
        
        
    def _parse_setts(self, setts):
        acc_json = self._parse_var(setts["account_json"])
        if acc_json is not None:
            self._accounts = acc.AccountArray(acc_json)
        
        asset_json = self._parse_var(setts["asset_json"])
        if asset_json is not None:
            self._assets = asse.AssetArray(asset_json)
        
        
        return self
        
    @property
    def accounts(self):
        return self._accounts
        
    @property
    def assets(self):
        return self._assets

import portfolio as pf
import portfolio.account as acc
import portfolio.asset as asse
import pandas as pd

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
        
    @property
    def asset_holdings(self):
        all_hold_acc = [a.asset_holdings.set_index("asset_name") for a in self.accounts.values()]
        df0 = all_hold_acc[0]
        if len(all_hold_acc)>1:
            for df1 in all_hold_acc[1:]:
                df0 = df0.add(df1,fill_value=0.0)
        
        df0.reset_index(inplace=True)
        return df0
        
    @property
    def account_holdings(self):
        all_hold_acc = [(an, av.asset_holdings["value"].sum()) for an, av in self.accounts.items()]
        return pd.DataFrame(all_hold_acc, columns = ["account_name","value"])
        
    @property
    def total_value(self):
        return self.account_holdings["value"].sum()
        
    def _collect_asset_attribute_scalar(self, attr_name):
        holds = self.asset_holdings.copy()
        holds[attr_name] = [getattr(self.assets[an], attr_name) for an in holds["asset_name"].values]
        
        coll = {attr_name:[], "value" : []} 
        for av, dfi in holds.groupby(attr_name):
            coll[attr_name].append(av)
            coll["value"].append(dfi["value"].sum())
            
        return pd.DataFrame(coll)
        
    def _collect_asset_attribute_dataframe(self, attr_name, attr_to_collect_name):
        holds = self.asset_holdings #.copy()
        all_df = []
        for an, av in zip(holds["asset_name"], holds["value"]):
            df = getattr(self.assets[an], attr_name).copy()
            df["value"] = df["weight"] * av
            all_df.append(df)
        
        df_col = pd.concat(all_df)
        
        coll = {attr_to_collect_name:[], "value" : []} 
        for av, dfi in df_col.groupby(attr_to_collect_name):
            coll[attr_to_collect_name].append(av)
            coll["value"].append(dfi["value"].sum())
            
        return pd.DataFrame(coll)
        
    def collect_risk_class(self):
        return self._collect_asset_attribute_scalar("risk_class")
        
        
    def collect_country(self):
        return self._collect_asset_attribute_dataframe("geographic_region", "country")
        

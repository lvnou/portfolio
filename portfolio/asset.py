import portfolio as pf

class AssetHandler(pf.SettedBaseHandler):
    def __init__(self, *args, **kwargs):
        self._type_dict = {
            "MUTUAL_FUND" : MutualFund,
            "EXCHANGE_TRADED_FUND" : ExchangeTradedFund,
            "CASH" : Cash 
         }
        return super(AssetHandler, self).__init__(*args, **kwargs)

class AssetArray(pf.SettedBaseArray):
    def __init__(self, *args, **kwargs):
        super(AssetArray,self).__init__(array_type_handler = AssetHandler, *args, **kwargs)

class Asset(pf.SettedBaseclass):
    pass
    

class Security(Asset):
    pass
    
class Cash(Asset):
    pass
    
class MutualFund(Security):
    pass
    
class ExchangeTradedFund(Security):
    pass
    
    
 
		
    

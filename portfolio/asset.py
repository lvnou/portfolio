import portfolio as pf
import pandas as pd

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
    """
    Representing an asset
    
    Attributes
    ----------
    risk_class : int
        Risk class, one of
        * 0 - Liquid, availible without risk
        * 1 - Low-risk bonds (government), self-owned real estate
        * 2 - Higher-risk bonds, mutual funds with stocks + bonds
        * 3 - Mutual funds in stocks, ETF, Index funds
        * 4 - Individual stock
        * 5 - Derivates etc.
    
    geographic_region : pd.DataFrame
        Represents the allocation of the asset by  geographic region.
        This DataFrame has the columns "country", "continent" and "weight" representing the according parameters.
    """
    # Risk
    _default_risk_class = None
    _risk_class = None
    # Geographic region
    _default_country_name = "unknown"
    _default_continent_name = "unknown"
    
    def __init__(self, *args, **kwargs):
        self._default_setts.update({
                                    "risk_class" : self._default_risk_class,
                                    "geographic_region" : dict()
                                    })
        return super(Asset, self).__init__(*args, **kwargs)
        

    def _one_region(self, country = None, continent = None):
        if country is None:
            country = self._default_country_name
        if continent is None:
            continent = self._default_continent_name
         
        self._region_df = pd.DataFrame({"country" : [country],
                                   "continent" : [continent],
                                   "weight"    : [1.0]})
        return self

    def _region_from_file(self, file):
        fname = self._parse_var(file)
        cols = {"Weight" : "weight", "Country": "country", "Continent": "continent"}
        df = self._parse_df_from_text(open(fname,"r").read(), cols=cols)

        df["weight"] = pd.to_numeric(df["weight"], downcast = "float")
        
        self._region_df = df
        return self

    def _init_region(self, file = None, *args, **kwargs):
        if file is not None:
            return self._region_from_file(file = file)
        return self._one_region(*args, **kwargs)

    def _parse_setts(self, setts):
        risk_class = self._parse_var(setts["risk_class"])
        self._risk_class = risk_class
        self._init_region(**setts["geographic_region"])
        
        return self
        
    @property
    def risk_class(self):
        return self._risk_class
    
    @property
    def geographic_region(self):
        return self._region_df
    

class Security(Asset):
    _default_issuer = "unknown"
    _issuer = None
    
    def __init__(self, *args, **kwargs):
        self._default_setts.update({
                                    "issuer" : self._default_issuer
                                    })
        return super(Security, self).__init__(*args, **kwargs)
        
    def _parse_setts(self, setts):
        self._issuer = self._parse_var(setts["issuer"])
        return super(Security, self)._parse_setts(setts)
        
    @property
    def issuer(self):
        return self._issuer
        
    
class Cash(Asset):
    _default_risk_class = 0
    
class MutualFund(Security):
    def __init__(self, *args, **kwargs):
        self._default_risk_class = 2
        return super(MutualFund, self).__init__(*args, **kwargs)
    
class ExchangeTradedFund(Security):
    _default_risk_class = 3
    
    
 
		
    

import portfolio as pf
import pandas as pd
import numpy as np
import warnings
import investpy

def interpolate_datetime(x, xp, yp):
    """
    Interpolate values where `x` values are given as a `datetime`
    """
    xpc = np.array(xp, dtype="float")
    xc = np.array(x, dtype="float")
    return np.interp(xc, xpc, yp)

class AssetPerformanceHandler(pf.SettedBaseHandler):
    def __init__(self, *args, **kwargs):
        self._type_dict = {
            "NOT_AVAILABLE" : NotAvailableAssetPerformance,
            "INVESTINGCOM" : InvestingComAssetPerformance,
            "DEKA_CSV" : DekaCSVAssetPerformance 
         }
        return super(AssetPerformanceHandler, self).__init__(*args, **kwargs)

class AssetPerformance(pf.SettedBaseclass):
    """
    Representing an assets performance
    """

    def __init__(self, *args, **kwargs):
       # self._default_setts.update({
        #                            "risk_class" : self._default_risk_class,
         #                           "geographic_region" : dict()
          #                          })
        return super(AssetPerformance, self).__init__(*args, **kwargs)
        
    def _calc_price(self, dates):
        raise NotImplementedError("Abstract class")

    def price(self, from_date, to_date, n = 20):
        d = pd.date_range(start=from_date, end=to_date,  periods=n)
        return self._calc_price(d), d

    def value(self, *args, relative_to = "LAST", **kwargs):
        p, d = self.price(*args, **kwargs)
        if relative_to == "LAST":
            p = p/p[-1]
        else:
            raise ValueError("relative_to")
        return p, d

class NotAvailableAssetPerformance(AssetPerformance):
    def _calc_price(self, dates):
        warnings.warn("Asset performance not available. Assuming constant price of unity.")
        return np.ones(dates.shape)

class InvestingComAssetPerformance(AssetPerformance):
    _ic_api_timefmt = "%d/%m/%Y"
    _ic_api_pricecol = "Close"

    def __init__(self, *args, **kwargs):
        self._default_setts.update({ "search_args" : dict() })
        return super(InvestingComAssetPerformance, self).__init__(*args, **kwargs)

    def _parse_setts(self, setts):
        self._search_args = self._parse_var(setts["search_args"])
        return self

    def _calc_price(self, dates):
        sr = investpy.search_quotes(**self._search_args)
        if len (sr) > 1:
            warnings.warn(f"investing.com API: More than one result found, choosing first one.\nArgs: {self._search_args}\nFound: {sr[0]}")
        elif len(sr) == 0:
            raise ValueError(f"investing.com API: No result found.\nArgs: {self._search_args}")
        srd = sr[0].retrieve_historical_data(   from_date = min(dates).strftime(self._ic_api_timefmt),
                                                to_date   = max(dates).strftime(self._ic_api_timefmt) )
        return interpolate_datetime(dates, srd.index, srd[self._ic_api_pricecol])

class DekaCSVAssetPerformance(AssetPerformance):
    pass

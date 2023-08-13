import portfolio as pf
import pandas as pd
import numpy as np
import warnings
import investpy
import tessa

# directory for bf4py needs to be added to python path
try:
    import bf4py
except ImportError:
    warnings.warn("Could not import bf4py. Can't use BoerseFrankfurtAssetPerformance interface.")


def interpolate_datetime(x, xp, yp):
    """
    Interpolate values where `x` values are given as a `datetime`
    """
    xpc = np.array(xp, dtype="float")
    xc = np.array(x, dtype="float")
    if (xc.min() < xpc.min()) or (xc.max() > xpc.max()):
        warnings.warn("interpolate_datetime: Requested x values are not in given xp bounds. Constant np.interp continuation assumed.")
    # remove unplausible values
    tol = np.median(yp) * 100
    if np.any(yp>tol):
        warnings.warn(f"interpolate_datetime: Removing {(yp>tol).sum()} outliers.")
    xpc = xpc[yp<tol]
    yp = yp[yp<tol]
    return np.interp(xc, xpc, yp)

class AssetPerformanceHandler(pf.SettedBaseHandler):
    def __init__(self, *args, **kwargs):
        self._type_dict = {
            "NOT_AVAILABLE" : NotAvailableAssetPerformance,
            "INVESTINGCOM" : InvestingComAssetPerformance,
            "DEKA_CSV" : DekaCSVAssetPerformance,
            "BOERSEFRANKFURT" : BoerseFrankfurtAssetPerformance,
            "CRYPTO" : CryptoCurrencyAssetPerformance
            }
        return super(AssetPerformanceHandler, self).__init__(*args, **kwargs)

class AssetPerformance(pf.SettedBaseclass):
    """
    Representing an assets performance
    """

    _default_col_name_price = "price"

    def __init__(self, *args, **kwargs):
        self._prices = dict()
        self._cache_price = True
        return super(AssetPerformance, self).__init__(*args, **kwargs)
        
    def _calc_price(self, dates):
        raise NotImplementedError("Abstract class")

    def price(self, from_date = None, to_date = None, n = 20):
        "Use None to return the maximum price history, max detailed"
        calc_key = f"{from_date}_{to_date}_{n}"
        if (from_date is None) or (to_date is None):
            d = None
        else:
            d = pd.date_range(start=from_date, end=to_date,  periods=n)
        if (calc_key not in self._prices) or (not self._cache_price):
            self._prices[calc_key] = self._calc_price(d)
        return self._prices[calc_key]

    def _get_col_name_price(self, name):
        return name

    def price_df(self, *args, col_name = None, **kwargs):
        p, d = self.price(*args, **kwargs)
        if col_name is None:
            col_name = self._default_col_name_price
        return pd.DataFrame(data={self._get_col_name_price(col_name):p}, index=d)

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
        return np.ones(dates.shape), dates

class InvestingComAssetPerformance(AssetPerformance):
    _ic_api_timefmt = "%d/%m/%Y"
    _ic_api_pricecol = "Close"
    _ic_api_pricecol_tessa = "close"
    _use_tessa = True
    _default_col_name_price = "$(isin)_price"

    def __init__(self, *args, **kwargs):
        self._default_setts.update({ "search_args" : dict() })
        return super(InvestingComAssetPerformance, self).__init__(*args, **kwargs)

    def _parse_setts(self, setts):
        self._search_args = self._parse_var(setts["search_args"])
        return self

    def _check_num_items(self, sr):
        if len (sr) > 1:
            warnings.warn(f"investing.com API: More than one result found, choosing first one.\nArgs: {self._search_args}\nFound: {sr[0]}")
        elif len(sr) == 0:
            raise ValueError(f"investing.com API: No result found.\nArgs: {self._search_args}")
        return self

    def _calc_price_investpy(self, dates):
        sr = investpy.search_quotes(**self._search_args)
        self._check_num_items(sr)
        srd = sr[0].retrieve_historical_data(   from_date = min(dates).strftime(self._ic_api_timefmt),
                                                to_date   = max(dates).strftime(self._ic_api_timefmt) )
        return interpolate_datetime(dates, srd.index, srd[self._ic_api_pricecol]), dates

    def _get_tessa_args(self):
        return [self._search_args['isin']], dict()

    def _calc_price_tessa(self, dates):
        a, kwa = self._get_tessa_args()
        sr = tessa.Symbol(*a, **kwa).price_history()
        if dates is None:
            return sr.df[self._ic_api_pricecol_tessa].to_numpy(), sr.df.index
        return interpolate_datetime(dates, sr.df.index, sr.df[self._ic_api_pricecol_tessa]), dates

    def _calc_price(self, dates):
        try:
            if self._use_tessa:
                return self._calc_price_tessa(dates)
            return self._calc_price_investpy(dates)
        except Exception as ex:
            warnings.warn(f"Failed to query performance for {self._search_args}. Exception: {ex}.")
        return NotAvailableAssetPerformance._calc_price(self, dates)

    def _get_col_name_price(self, name):
        for k, v in self._search_args.items():
            name = name.replace(f"$({k})", v)
        return name

class CryptoCurrencyAssetPerformance(InvestingComAssetPerformance):
    _default_col_name_price = "$(symbol)_price"
    def _get_tessa_args(self):
        return [self._search_args['name']], {"source":"coingecko"}


class DekaCSVAssetPerformance(AssetPerformance):
    """
    CSV file as can be exported from deka.de
    """
    _deka_pricecol = "Ausgabepreis"
    _deka_timecol = "Datum"

    def __init__(self, *args, **kwargs):
        self._default_setts.update({ "csv_file_path" : "" })
        return super(DekaCSVAssetPerformance, self).__init__(*args, **kwargs)

    def _parse_setts(self, setts):
        self._csv_file = self._parse_var(setts["csv_file_path"])
        return self

    def _calc_price(self, dates):
        data = pd.read_csv(self._csv_file, encoding='latin-1', sep=";", decimal=",")
        data[self._deka_timecol] = pd.to_datetime(data[self._deka_timecol])
        return interpolate_datetime(dates, data[self._deka_timecol], data[self._deka_pricecol]), dates


class BoerseFrankfurtAssetPerformance(AssetPerformance):
    """
    https://github.com/joqueka/bf4py
    NOT MAINTAINED / TESTED!!
    """
    def _parse_setts(self, setts):
        self._isin = self._parse_var(setts["isin"])
        return self

    def _calc_price(self, dates):
        history = bf4py.general.eod_data(self._isin, min(dates), max(dates))
        history_df = pd.DataFrame(history)
        history_df['date']= pd.to_datetime(history_df['date'])
        return interpolate_datetime(dates, history_df['date'], history_df['close']), dates



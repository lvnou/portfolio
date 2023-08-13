import portfolio as pf
import portfolio.asset_performance as apf
import pytest
from .util import get_test_path
import warnings
import numpy as np

search_args = [ 
    {"wkn" : "A0YEDG", "isin":"IE00B5BMR087"},
    {"wkn" : "A0YEDK", "isin":"IE00B53L4350"}
        ]

search_args_invalid = [ 
        {"test":""},
        ]


def test_notavai_performance():
    na = apf.NotAvailableAssetPerformance(setts=dict())
    p,d = na.price("2021-1-1","2022-1-1", 20)
    assert d.size == 20
    assert p.size == 20
    assert p[-1] == 1.
    v,d = na.value("2021-1-1","2022-1-1", 20)
    assert v.size == 20
    assert v[-1] == 1.

@pytest.mark.parametrize("search_args", search_args)
def test_investcom_performance(search_args):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        ic = apf.InvestingComAssetPerformance(setts={"search_args": search_args})
        p,d = ic.price("2021-1-1","2022-1-1", 20)
        assert p.size == 20
        assert np.any(p != 1.)

@pytest.mark.parametrize("search_args", search_args_invalid)
def test_investcom_performance_invalid(search_args):
    with pytest.warns(UserWarning):
        ic = apf.InvestingComAssetPerformance(setts={"search_args": search_args})
        p,d = ic.price("2021-1-1","2022-1-1", 20)
        assert p.size == 20
        assert np.all(p == 1.)


#def test_boersefrankfurt_performance():
#    fn = apf.BoerseFrankfurtAssetPerformance(setts={"isin": 'DE0008404005'})
#    p,d = fn.price("2021-1-1","2022-1-1", 20)
#    print(p,d)
#    assert p.size == 20

def test_dekacsv_performance():
    fn = apf.DekaCSVAssetPerformance(setts={"csv_file_path": get_test_path('06_test_asset_performance/DE0008474750_Preisexport.csv')})
    p,d = fn.price("2021-1-1","2022-1-1", 20)
    assert p.size == 20

def test_dekacsv_performance_outofrange():
    fn = apf.DekaCSVAssetPerformance(setts={"csv_file_path": get_test_path('06_test_asset_performance/DE0008474750_Preisexport.csv')})
    p,d = fn.price("2016-1-1","2022-1-1", 20)
    assert p.size == 20

def test_performance_handler():
    pfh = apf.AssetPerformanceHandler(setts = {"type": "NOT_AVAILABLE"}).get()
    assert isinstance(pfh, apf.NotAvailableAssetPerformance)

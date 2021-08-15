import portfolio as pf
import portfolio.asset as asse
import pytest
import pandas as pd
import pandas.testing as pdt


anames = ["ETF_1", "ETF_2", "MF_1"]
rks = [3,3,2]
region_dfs = [
                pd.DataFrame({"country" : ["Germany"], "continent" : ["Europe"],  "weight" : [1.0]}),
                pd.DataFrame({"country" : ["Germany","China","USA"], "continent" : ["Europe","Asia","North America"],  "weight" : [0.5,0.25,0.25]}),
                pd.DataFrame({"country" : ["USA"], "continent" : ["North America"],  "weight" : [1.0]}),
 ]
 

def test_initialize_assets():
    a = asse.AssetArray("03_test_asset_with_values/assets.json")
    assert isinstance(a["ETF_1"], asse.ExchangeTradedFund)
    assert isinstance(a["MF_1"], asse.MutualFund)

@pytest.mark.parametrize("aname, rkexp", zip(anames, rks))
def test_risk_class(aname, rkexp):
    aa = asse.AssetArray("03_test_asset_with_values/assets.json")
    rk = aa[aname].risk_class
    assert rk == rkexp

@pytest.mark.parametrize("aname, region_df", zip(anames, region_dfs)) 
def test_geographic_region(aname, region_df):
    aa = asse.AssetArray("03_test_asset_with_values/assets.json")
    reg  = aa[aname].geographic_region
    pdt.assert_frame_equal(reg, region_df, check_dtype = False, check_like = True)


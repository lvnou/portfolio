import portfolio as pf
import portfolio.account as acc
import pytest
import pandas as pd
import pandas.testing as pdt
import numpy as np

account_names = ["Account_1", "Account_2"]
assets = [['ETF_1', 'ETF_2', 'LIQUID'], ["ETF_1","MF_1","LIQUID"]]
holds = [
            pd.DataFrame({"asset_name" : assets[0], "value": [1002.0,1001.0,12.0]}),
            pd.DataFrame({"asset_name" : assets[1], "value": [102.0, 10000.0-50., 120000.0]}),
      ]



def test_initialize_accounts():
    a = acc.AccountArray("02_test_account/account/accounts.json")
    assert isinstance(a["Account_1"], acc.BankAccount)
    assert isinstance(a["Account_2"], acc.BankAccount)
    
@pytest.mark.parametrize("aname, asse", zip(account_names, assets))
def test_assets_in_account(aname, asse):
    aa = acc.AccountArray("04_test_asset_and_account/account/accounts.json")
    assert set([*aa[aname].asset_names]) == set([*asse])


@pytest.mark.parametrize("aname, hold", zip(account_names, holds))
def test_holdings_in_account(aname, hold):
    aa = acc.AccountArray("04_test_asset_and_account/account/accounts.json")
    pdt.assert_frame_equal(aa[aname].asset_holdings, hold, check_dtype=False, check_like = True)


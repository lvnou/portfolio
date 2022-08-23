import portfolio as pf
import portfolio.portfolio as portfolio
import portfolio.account as acc
import portfolio.asset as asse
import portfolio.transaction as tr

import numpy as np
import pandas as pd
import pandas.testing as pdt
from .util import get_test_path
import pytest

def test_initialize_portfolio():
    p = portfolio.PortfolioHandler(get_test_path("01_test_portfolio/portfolio.json")).get()
    assert isinstance(p, portfolio.Portfolio)
    
    
def test_initialize_accounts_portfolio():
    p = portfolio.PortfolioHandler(get_test_path("02_test_account/portfolio.json")).get()
    a = p.accounts
    assert len(a) == 2
    assert isinstance(a["Account_1"], acc.BankAccount)
    
    
def test_account_transactions():
    p = portfolio.PortfolioHandler(get_test_path("02_test_account_transactions/portfolio.json")).get()
    a = p.accounts
    assert len(a) == 2
    
    a1 = a["Account_1"]
    t1 = a1.transactions
    a2 = a["Account_2"]
    t2 = a2.transactions
    
    assert isinstance(t1, tr.TransactionStatement)
    assert isinstance(t2, tr.TransactionStatement)
    
def test_initialize_assets_portfolio():
    p = portfolio.PortfolioHandler(get_test_path("03_test_asset/portfolio.json")).get()
    a = p.assets
    assert len(a) == 3
    

def test_total_value_portfolio():
    p = portfolio.PortfolioHandler(get_test_path("04_test_asset_and_account/portfolio.json")).get()
    assert p.total_value == 132067.0 
    
def test_asset_holdings_in_portfolio():
    p = portfolio.PortfolioHandler(get_test_path("04_test_asset_and_account/portfolio.json")).get()
    expected_df = pd.DataFrame({"asset_name":["ETF_1","ETF_2","LIQUID","MF_1"], "value" : [1104.,1001.,120012.,9950.]})
    pdt.assert_frame_equal(p.asset_holdings, expected_df, check_dtype=False, check_like = True)

def test_account_holdings_in_portfolio():
    p = portfolio.PortfolioHandler(get_test_path("04_test_asset_and_account/portfolio.json")).get()
    expected_df = pd.DataFrame({"account_name":["Account_1","Account_2"], "value" : [2015.0, 130052.0]})
    pdt.assert_frame_equal(p.account_holdings, expected_df, check_dtype=False, check_like = True)

def test_account_holdings_in_portfolio2():
    p = portfolio.PortfolioHandler(get_test_path("04_test_asset_and_account_2/portfolio.json")).get()
    expected_df = pd.DataFrame({"account_name":["Account_1","Account_2"], "value" : [2014.0, 130052.0]})
    pdt.assert_frame_equal(p.account_holdings, expected_df, check_dtype=False, check_like = True)

def test_collect_risk_class_portfolio():
    p = portfolio.PortfolioHandler(get_test_path("04_test_asset_and_account/portfolio.json")).get()
    df_risk = p.collect_risk_class()
    expected_df = pd.DataFrame({"risk_class":[0,2,3],"value":[120012.0,9950.0,2105.0]})
    pdt.assert_frame_equal(df_risk, expected_df, check_dtype=False, check_like = True)

def test_collect_country_portfolio():
    p = portfolio.PortfolioHandler(get_test_path("04_test_asset_and_account/portfolio.json")).get()
    df_count = p.collect_country()
    expected_df = pd.DataFrame({"country":["China","Germany","USA","unknown"],"value":[250.25,1604.50,10200.25,120012.00]})
    pdt.assert_frame_equal(df_count, expected_df, check_dtype=False, check_like = True)

def test_collect_performance():
    expected = {'ETF_1': (np.array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1.]), pd.DatetimeIndex([          '2021-01-01 00:00:00',
               '2021-01-20 05:03:09.473684210',
               '2021-02-08 10:06:18.947368421',
               '2021-02-27 15:09:28.421052632',
               '2021-03-18 20:12:37.894736842',
               '2021-04-07 01:15:47.368421052',
               '2021-04-26 06:18:56.842105264',
               '2021-05-15 11:22:06.315789474',
               '2021-06-03 16:25:15.789473684',
               '2021-06-22 21:28:25.263157894',
               '2021-07-12 02:31:34.736842104',
               '2021-07-31 07:34:44.210526316',
               '2021-08-19 12:37:53.684210528',
               '2021-09-07 17:41:03.157894736',
               '2021-09-26 22:44:12.631578948',
               '2021-10-16 03:47:22.105263156',
               '2021-11-04 08:50:31.578947368',
               '2021-11-23 13:53:41.052631580',
               '2021-12-12 18:56:50.526315788',
                         '2022-01-01 00:00:00'],
              dtype='datetime64[ns]', freq=None)), 'ETF_2': (np.array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1.]), pd.DatetimeIndex([          '2021-01-01 00:00:00',
               '2021-01-20 05:03:09.473684210',
               '2021-02-08 10:06:18.947368421',
               '2021-02-27 15:09:28.421052632',
               '2021-03-18 20:12:37.894736842',
               '2021-04-07 01:15:47.368421052',
               '2021-04-26 06:18:56.842105264',
               '2021-05-15 11:22:06.315789474',
               '2021-06-03 16:25:15.789473684',
               '2021-06-22 21:28:25.263157894',
               '2021-07-12 02:31:34.736842104',
               '2021-07-31 07:34:44.210526316',
               '2021-08-19 12:37:53.684210528',
               '2021-09-07 17:41:03.157894736',
               '2021-09-26 22:44:12.631578948',
               '2021-10-16 03:47:22.105263156',
               '2021-11-04 08:50:31.578947368',
               '2021-11-23 13:53:41.052631580',
               '2021-12-12 18:56:50.526315788',
                         '2022-01-01 00:00:00'],
              dtype='datetime64[ns]', freq=None)), 'MF_1': (np.array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1.]), pd.DatetimeIndex([          '2021-01-01 00:00:00',
               '2021-01-20 05:03:09.473684210',
               '2021-02-08 10:06:18.947368421',
               '2021-02-27 15:09:28.421052632',
               '2021-03-18 20:12:37.894736842',
               '2021-04-07 01:15:47.368421052',
               '2021-04-26 06:18:56.842105264',
               '2021-05-15 11:22:06.315789474',
               '2021-06-03 16:25:15.789473684',
               '2021-06-22 21:28:25.263157894',
               '2021-07-12 02:31:34.736842104',
               '2021-07-31 07:34:44.210526316',
               '2021-08-19 12:37:53.684210528',
               '2021-09-07 17:41:03.157894736',
               '2021-09-26 22:44:12.631578948',
               '2021-10-16 03:47:22.105263156',
               '2021-11-04 08:50:31.578947368',
               '2021-11-23 13:53:41.052631580',
               '2021-12-12 18:56:50.526315788',
                         '2022-01-01 00:00:00'],
              dtype='datetime64[ns]', freq=None)), 'LIQUID': (np.array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1.]), pd.DatetimeIndex([          '2021-01-01 00:00:00',
               '2021-01-20 05:03:09.473684210',
               '2021-02-08 10:06:18.947368421',
               '2021-02-27 15:09:28.421052632',
               '2021-03-18 20:12:37.894736842',
               '2021-04-07 01:15:47.368421052',
               '2021-04-26 06:18:56.842105264',
               '2021-05-15 11:22:06.315789474',
               '2021-06-03 16:25:15.789473684',
               '2021-06-22 21:28:25.263157894',
               '2021-07-12 02:31:34.736842104',
               '2021-07-31 07:34:44.210526316',
               '2021-08-19 12:37:53.684210528',
               '2021-09-07 17:41:03.157894736',
               '2021-09-26 22:44:12.631578948',
               '2021-10-16 03:47:22.105263156',
               '2021-11-04 08:50:31.578947368',
               '2021-11-23 13:53:41.052631580',
               '2021-12-12 18:56:50.526315788',
                         '2022-01-01 00:00:00'],
              dtype='datetime64[ns]', freq=None))}
    
    p = portfolio.PortfolioHandler(get_test_path("04_test_asset_and_account/portfolio.json")).get()
    cp= p.collect_performance("2021-1-1","2022-1-1", 20)
    assert cp.keys() == expected.keys()
    assert np.all(cp['LIQUID'][1] ==  expected['LIQUID'][0]*120012.)
    assert np.all(cp['LIQUID'][0] ==  expected['LIQUID'][1])

@pytest.mark.parametrize("pname", ["04_test_asset_and_account/portfolio.json", "05_test_portfolio_performance/portfolio.json"])
def test_collect_performance_check_only_len(pname):
    p = portfolio.PortfolioHandler(get_test_path(pname)).get()
    cp= p.collect_performance("2021-1-1","2022-1-1", 20)
    assert cp['LIQUID'][1].size ==  20
    assert cp['LIQUID'][0].size ==  20

def test_total_performance_portfolio():
    p = portfolio.PortfolioHandler(get_test_path("04_test_asset_and_account/portfolio.json")).get()
    cp_d, cp_p = p.total_performance("2021-1-1","2022-1-1", 20)
    assert np.all(cp_p == np.array([132067., 132067., 132067., 132067., 132067., 132067., 132067.,
       132067., 132067., 132067., 132067., 132067., 132067., 132067.,
       132067., 132067., 132067., 132067., 132067., 132067.]))


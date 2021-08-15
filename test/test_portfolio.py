import portfolio as pf
import portfolio.portfolio as portfolio
import portfolio.account as acc
import portfolio.asset as asse
import portfolio.transaction as tr
import pandas as pd
import pandas.testing as pdt

def test_initialize_portfolio():
    p = portfolio.PortfolioHandler("01_test_portfolio/portfolio.json").get()
    assert isinstance(p, portfolio.Portfolio)
    
    
def test_initialize_accounts_portfolio():
    p = portfolio.PortfolioHandler("02_test_account/portfolio.json").get()
    a = p.accounts
    assert len(a) == 2
    assert isinstance(a["Account_1"], acc.BankAccount)
    
    
def test_account_transactions():
    p = portfolio.PortfolioHandler("02_test_account_transactions/portfolio.json").get()
    a = p.accounts
    assert len(a) == 2
    
    a1 = a["Account_1"]
    t1 = a1.transactions
    a2 = a["Account_2"]
    t2 = a2.transactions
    
    assert isinstance(t1, tr.TransactionStatement)
    assert isinstance(t2, tr.TransactionStatement)
    
def test_initialize_assets_portfolio():
    p = portfolio.PortfolioHandler("03_test_asset/portfolio.json").get()
    a = p.assets
    assert len(a) == 3
    
    
def test_asset_holdings_in_portfolio():
    p = portfolio.PortfolioHandler("04_test_asset_and_account/portfolio.json").get()
    expected_df = pd.DataFrame({"asset_name":["ETF_1","ETF_2","LIQUID","MF_1"], "value" : [1104.,1001.,120012.,9950.]})
    pdt.assert_frame_equal(p.asset_holdings, expected_df, check_dtype=False, check_like = True)

def test_account_holdings_in_portfolio():
    p = portfolio.PortfolioHandler("04_test_asset_and_account/portfolio.json").get()
    expected_df = pd.DataFrame({"account_name":["Account_1","Account_2"], "value" : [2015.0, 130052.0]})
    pdt.assert_frame_equal(p.account_holdings, expected_df, check_dtype=False, check_like = True)


def test_collect_risk_class_portfolio():
    p = portfolio.PortfolioHandler("04_test_asset_and_account/portfolio.json").get()
    df_risk = p.collect_risk_class()
    expected_df = pd.DataFrame({"risk_class":[0,2,3],"value":[120012.0,9950.0,2105.0]})
    pdt.assert_frame_equal(df_risk, expected_df, check_dtype=False, check_like = True)

def test_collect_country_portfolio():
    p = portfolio.PortfolioHandler("04_test_asset_and_account/portfolio.json").get()
    df_count = p.collect_country()
    expected_df = pd.DataFrame({"country":["China","Germany","USA","unknown"],"value":[250.25,1604.50,10200.25,120012.00]})
    pdt.assert_frame_equal(df_count, expected_df, check_dtype=False, check_like = True)


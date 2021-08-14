import portfolio as pf
import portfolio.portfolio as portfolio
import portfolio.account as acc
import portfolio.asset as asse

def test_initialize_portfolio():
    p = portfolio.PortfolioHandler("01_test_portfolio/portfolio.json").get()
    assert isinstance(p, portfolio.Portfolio)
    
    
def test_initialize_accounts():
    p = portfolio.PortfolioHandler("02_test_account/portfolio.json").get()
    a = p.accounts
    assert len(a) == 2
    assert isinstance(a["Account_1"], acc.BankAccount)
    
    
def test_initialize_assets():
    p = portfolio.PortfolioHandler("03_test_asset/portfolio.json").get()
    a = p.assets
    assert len(a) == 3
    assert isinstance(a["ETF_1"], asse.ExchangeTradedFund)
    assert isinstance(a["MF_1"], asse.MutualFund)

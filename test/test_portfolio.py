import portfolio as pf
import portfolio.portfolio as portfolio

def test_initialize_portfolio():
    p = portfolio.PortfolioHandler("test_p/portfolio.json").get()
    assert isinstance(p, portfolio.Portfolio)
    
    
def test_initialize_accounts():
    p = portfolio.PortfolioHandler("test_a/portfolio.json").get()
    a = p.accounts
    assert len(a) == 2

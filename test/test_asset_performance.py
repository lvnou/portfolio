import portfolio as pf
import portfolio.asset_performance as apf
import pytest

search_args = [
        {'text' : 'a14utf'}, # 2 results
        {'text' : 'deka us treasury'} # 1 result
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
    ic = apf.InvestingComAssetPerformance(setts={"search_args": search_args})
    p,d = ic.price("2021-1-1","2022-1-1", 20)
    assert p.size == 20

def test_performance_handler():
    pfh = apf.AssetPerformanceHandler(setts = {"type": "NOT_AVAILABLE"}).get()
    assert isinstance(pfh, apf.NotAvailableAssetPerformance)

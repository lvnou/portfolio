import portfolio.transaction as tr
import pytest
from datetime import date
import pandas as pd
import pandas.testing as pdt


t_files = ["02_test_account_transactions/account/trans_acc_1.txt","02_test_account_transactions/account/trans_acc_2.txt"]

sdfs = [
            pd.DataFrame( { "asset_name" : ["ETF_1","ETF_1","ETF_1","ETF_2","LIQUID"],
                            "date"       : [date(2021,1,1), date(2021,2,1), date(2021,5,11), date(2022,1,1), date(2022,1,1)],
                            "value"      :  [0.0, 1000.0, 1002.0, 1001.0, 12.0]
                            }),
            pd.DataFrame( { "asset_name" : ["ETF_1","ETF_1","ETF_1","MF_2","LIQUID"],
                            "date"       : [date(2021,1,1), date(2021,2,1), date(2021,5,11), date(2022,1,1), date(2022,1,1)],
                            "value"      :  [0.0, 100.0, 102.0, 10000.0, 120000.0]
                            })
        ]
        
tdfs = [
        pd.DataFrame( { "asset_name" : ["ETF_1","ETF_2"],
                            "date"       : [date(2021,2,1), date(2021,2,1)],
                            "value"      :  [1000.0, 1000.0]
                            }),
        pd.DataFrame( { "asset_name" : ["ETF_1","MF_1"],
                            "date"       : [date(2021,2,1), date(2021,2,1)],
                            "value"      :  [100.0, -50.0]
                            }),]

@pytest.mark.parametrize("t_file,sdf", zip(t_files, sdfs))
def test_read_transactions_status(t_file, sdf):
    t = tr.TransactionStatement().from_text_file(t_file)
    sdf["date"] = pd.to_datetime(sdf["date"])
    pdt.assert_frame_equal(t.status, sdf, check_dtype = False)
    
    
@pytest.mark.parametrize("t_file,tdf", zip(t_files, tdfs))    
def test_read_transactions_transactions(t_file, tdf):
    
    t = tr.TransactionStatement().from_text_file(t_file)
    print(t.transactions)
    tdf["date"] = pd.to_datetime(tdf["date"])
    pdt.assert_frame_equal(t.transactions, tdf, check_dtype = False)
    

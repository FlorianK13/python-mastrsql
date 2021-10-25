from mastrsql.mastr import Mastr
import pytest
import os
import pandas as pd


def test_Mastr_init():
    with pytest.raises(AssertionError):
        user_credentials = "This is a string"
        mastr = Mastr(user_credentials=user_credentials)
 
    mastr = Mastr()
    #print(mastr.url)
    assert type(mastr.today) == str
    assert type(mastr.url) == str
    assert "marktstammdatenregister" in mastr.url



def test_Mastr_download():
    mastr = Mastr()
    mastr.download()
    assert os.path.exists(mastr.save_zip_path) 
    assert os.path.getsize(mastr.save_zip_path) > 900000000

def test_Mastr_to_sql():
    exclude_tables=[]
    mastr = Mastr()
    mastr.to_sql(exclude_tables=exclude_tables)

    df=pd.read_sql("netze", con = mastr.engine)
    assert type(df)==pd.core.frame.DataFrame
    assert len(df) >= 100

    df_2=pd.read_sql("einheitengaserzeuger", con = mastr.engine)
    assert type(df)==pd.core.frame.DataFrame
    assert len(df) >= 100



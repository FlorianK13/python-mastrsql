from mastrsql.mastr import Mastr
import pytest
import os
import pandas as pd


def test_Mastr_init():
    with pytest.raises(AssertionError):
        user_credentials = "This is a string"
        mastr = Mastr(user_credentials=user_credentials)
 
    mastr = Mastr()
    assert type(mastr.today) == str
    assert type(mastr.url) == str
    assert "marktstammdatenregister" in mastr.url



def test_Mastr_download():
    mastr = Mastr()
    mastr.download()
    assert os.path.exists(mastr.save_zip_path) 
    assert os.path.getsize(mastr.save_zip_path) > 900000000

def test_Mastr_to_sql():
    exclude_tables=["anlageneegsolar", "einheitensolar", "lokationen", "marktakteure", "netzanschlusspunkte","marktrollen"]
    include_tables=["netze","einheitengaserzeuger","marktrollen"]
    mastr = Mastr()
    mastr.to_sql(exclude_tables=exclude_tables)
    

    df=pd.read_sql("netze", con = mastr.engine)
    assert type(df)==pd.core.frame.DataFrame
    assert len(df) >= 100

    df_2=pd.read_sql("einheitengaserzeuger", con = mastr.engine)
    assert type(df_2)==pd.core.frame.DataFrame
    assert len(df_2) >= 100

    mastr.to_sql(include_tables=include_tables)
    df_3=df_2=pd.read_sql("marktrollen", con = mastr.engine)
    assert type(df_3)==pd.core.frame.DataFrame
    assert len(df_3) >= 100


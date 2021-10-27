from mastrsql.utils import get_url, correction_of_metadata
import pandas as pd
import numpy as np


def test_get_url():
    assert type(get_url()) == str


def test_correction_of_metadata():
    df = pd.DataFrame(
        {
            "Postleitzahl": [10000, "10001"],
            "Laengengrad": ["799.3",33.33],
            "Inbetriebnahmedatum": ["20201003","18001010"]
        }
    )
    sql_tablename = "einheitengasspeicher"
    df_2, sql_dtype_dict = correction_of_metadata(df,sql_tablename)

    assert type(df_2) == pd.core.frame.DataFrame
    assert len(df_2) == 2
    assert type(df_2.Postleitzahl[1]) == np.int32
    assert type(df_2.Inbetriebnahmedatum[1]) == pd._libs.tslibs.timestamps.Timestamp
    assert type(sql_dtype_dict) == dict
    assert len(sql_dtype_dict) == 3


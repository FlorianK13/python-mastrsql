import numpy as np
import os
from os.path import expanduser
from zipfile import ZipFile
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import pdb
import psycopg2
import lxml
import shutil
from mastrsql.utils import (
    get_url,
    download_from_url,
    correction_of_metadata,
    handle_xml_syntax_error,
    initialize_database,
)


class Mastr:
    """Mirrors the MaStR (Marktstammdatenregister) to a PostrgreSQL data base."""

    def __init__(self, user_credentials={}):
        self.user_credentials = user_credentials
        # self.today = date.today().strftime("%Y%m%d")
        self.today = 20211015
        self.url = get_url()
        self.save_path = os.path.join(
            expanduser("~"),
            ".mastrsql",
            "data",
        )
        self.save_zip_path = os.path.join(
            self.save_path, "Gesamtdatenexport_%s.zip" % self.today
        )

    def initialize(self):
        """Downloads the latest MaStR zipped file to ~/.mastrsql/data"""

        if os.path.exists(self.save_zip_path):
            print("MaStR already downloaded.")
        else:
            print("MaStR is downloaded to %s" % self.save_path)
            shutil.rmtree(self.save_path)
            os.makedirs(self.save_path, exist_ok=True)
            # download data from url
            download_from_url(self.url, self.save_zip_path, self.today)

    def to_sql(self):
        """Writes the local zipped MaStR to a PostgreSQL database"""
        initialize_database(self.user_credentials)

        engine = create_engine(
            "postgresql+psycopg2://postgres:postgres@localhost:5432/mastrsql"
        )

        # only relevant while coding, should be deleted before production built
        # filesthatwork = []

        filesthatwork = [
            "anlageneegbiomasse",
            "anlageneeggeosolarthermiegrubenklaerschlammdruckentspannung",
            "anlageneegsolar",
            "anlageneegspeicher",
            "anlageneegwasser",
            "anlageneegwind",
            "anlagengasspeicher",
            "anlagenkwk",
            "anlagenstromspeicher",
            "bilanzierungsgebiete",
            "einheitenbiomasse",
            "einheitengaserzeuger",
            "einheitengasspeicher",
            "einheitengasverbraucher",
            "einheitengenehmigung",
            "einheitengeosolarthermiegrubenklaerschlammdruckentspannung",
            "einheitenkernkraft",
            "einheitensolar",
            "lokationen",
            "marktakteure",
            "einheitenstromspeicher",
            "einheitenstromverbraucher",
            "einheitentypen",
        ]

        with ZipFile(self.save_zip_path, "r") as f:
            for name in f.namelist():
                # sql tablename is the beginning of the filename without the number in lowercase
                sql_tablename = name.split("_")[0].split(".")[0].lower()

                # check whether the table exists with current data and append new data or whether to overwrite the existing table
                if (
                    name.split(".")[0].split("_")[-1] == "1"
                    or len(name.split(".")[0].split("_")) == 1
                ):
                    if_exists = "replace"
                    print("New table is created!")
                else:
                    if_exists = "append"

                exist_count = filesthatwork.count(sql_tablename)
                if exist_count == 0:
                    opened_file = f.open(name)
                    data = f.read(name)
                    print(name, len(data))
                    save_path_metadata = os.path.join(self.save_path, "metadata")
                    try:
                        df = pd.read_xml(data, encoding="UTF-16", compression="zip")
                        df, sql_dtype_dict = correction_of_metadata(
                            df, sql_tablename, save_path_metadata
                        )

                    except lxml.etree.XMLSyntaxError as err:
                        df = handle_xml_syntax_error(data, err)
                        df, sql_dtype_dict = correction_of_metadata(
                            df, sql_tablename, save_path_metadata
                        )
                    continueloop = True

                    """Some files introduce new columns for existing tables. 
                    If this happens, the error from writing entries into non-existing columns is caught and the column is created."""
                    while continueloop:
                        try:
                            df.to_sql(
                                sql_tablename,
                                engine,
                                if_exists=if_exists,
                                dtype=sql_dtype_dict,
                            )
                            continueloop = False
                        except sqlalchemy.exc.ProgrammingError as err:
                            missing_column = str(err).split("«")[0].split("»")[1]
                            print("Altered table column " + missing_column)
                            con = psycopg2.connect(
                                "dbname=mastrsql user=postgres password='postgres'"
                            )
                            cursor = con.cursor()
                            execute_message = 'ALTER TABLE %s ADD "%s" text NULL;' % (
                                sql_tablename,
                                missing_column,
                            )
                            print(execute_message)
                            cursor.execute(execute_message)
                            con.commit()
                            cursor.close()
                            con.close()
                        except sqlalchemy.exc.DataError as err:
                            delete_entry = str(err).split("«")[0].split("»")[1]
                            print(delete_entry)
                            df = df.replace(delete_entry, np.nan)
                        except:
                            pdb.set_trace()


if __name__ == "__main__":
    database = Mastr()
    # database.initialize()
    database.to_sql()

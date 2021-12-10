from mastrsql.mastr import Mastr

postgres_standard_credentials = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        }

database = Mastr(postgres_standard_credentials=postgres_standard_credentials)
database.download()

include_tables=["netze","einheitengaserzeuger","marktrollen"]

database.to_sql(include_tables=include_tables)
print("FINISHED")

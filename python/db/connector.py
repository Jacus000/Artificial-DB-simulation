from sqlalchemy import create_engine
import mysql.connector
import urllib.parse
import os

# Warto by było stworzyć .env żeby nie było widać danych logowania w kodzie po push na github

# Łączność z serwerem i bazą
def get_db_config():
    # host = os.environ.get("DB_HOST")
    # user = os.environ.get("DB_USER")
    # password = os.environ.get("DB_PASSWORD")
    # database = os.environ.get("DB_DATABASE")
    return "giniewicz.it", "team05", "te@mzos" ,"team05"


# Łączenie z serwerem i bazą do współpracy z Pandasem (w taki sposób łatwiej niż przez cursor)
def get_engine():
    host, user, password, database = get_db_config()
    password = urllib.parse.quote_plus(password)
    url = (f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    return create_engine(url, pool_recycle=3600)


# Łączenie pod cursor i query
def get_connection():
    host, user, password, database = get_db_config()
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
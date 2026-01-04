import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np


# Łącznie z bazą danych
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="giniewicz.it",
            user="team05",
            password="te@mzos",
            database="team05",
            port=3306
        )
        if conn.is_connected():
            return conn

    except Error as e:
        print(f"Błąd podczas łączenia z bazą danych: {e}")
        return None




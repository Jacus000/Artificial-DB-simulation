import os
from urllib.parse import quote_plus
from typing import Any
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Result
from dotenv import load_dotenv

load_dotenv()

class DataBaseAccess:

    _engine: Engine = None

    def __init__(self):
        if DataBaseAccess._engine == None:
            DataBaseAccess._engine = self.create_engine()
        
        self.engine = DataBaseAccess._engine

    def create_engine(self) -> Engine:
        USER = os.getenv("DB_USER")
        PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
        HOST = os.getenv("DB_HOST")
        PORT = os.getenv("DB_PORT")
        DATABASE = os.getenv("DB_NAME")

        if not all([USER, PASSWORD, DATABASE, PORT, HOST]):
            raise RuntimeError("Missing DB configuration in .env")
        
        return create_engine(f"mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    def execute(self, query: str) -> Result:
        try:
            with self.engine.connect() as conn:
                with conn.begin():
                    statements = query.split(';')
                    for statement in statements:
                        clean_stmt = statement.strip()
                        if clean_stmt:
                            conn.execute(text(clean_stmt))
        except Exception as e:
            print(f"Error while executing SQL query {e}")
            raise

    def insert_data(self, table_name: str, data: list[dict] | dict, chunk_size=1000):
        if not data:
            return

        if isinstance(data, dict):
            data = [data]

        columns = data[0].keys()
        
        col_names = ", ".join(columns)
        placeholders = ", ".join([f":{col}" for col in columns])
        
        query = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
       
        total_records = len(data)
        try:
            with self.engine.connect() as conn:

                for i in range(0, total_records, chunk_size):
                    chunk = data[i : i+chunk_size]
                    with conn.begin():
                        conn.execute(text(query), chunk)
                print(f"Pomyślnie wstawiono {len(data)} rekordów do tabeli '{table_name}'.")
        except Exception as e:
            print(f"Błąd podczas INSERT do tabeli {table_name}: {e}")
            raise
        
    def fetch_all(self, query: str) -> list[dict] | None:
        with self.engine.connect() as conn:
            try:
                result: Result = conn.execute(text(query))
                return [dict(row) for row in result.mappings()]
            except Exception as e:
                print(f"Blad laczenia albo cos innego {e}")
                return None
    
    def fetch_one(self, query: str) -> dict | None:
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            row = result.mappings().first()
            return dict(row) if row else None
    
    def fetch_scalar(self, query):
        with self.engine.connect() as conn:
            return conn.execute(text(query)).scalar()
        








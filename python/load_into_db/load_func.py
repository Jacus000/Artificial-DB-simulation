from python.db.connector import get_engine

"Przelanie danych z Pandasa do bazy danych na serwerze"
# table_name nazwa tabeli w bazie danych
def load_df_to_sql(df, table_name, engine = None):
    if engine is None:
        engine = get_engine()
    try:
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print("OK")
    except Exception as e:
        print(f"Błąd podczas połączenia: {e}. ")
    finally:
        engine.dispose()

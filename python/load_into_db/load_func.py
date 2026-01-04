from python.db.connector import get_engine

"Przelanie danych z Pandasa do bazy danych na serwerze"
def load_df_to_sql(df, df_name, engine = None):
    if engine is None:
        engine = get_engine()
    try:
        df.to_sql(df_name, con=engine, if_exists='append', index=False)
        print("OK")
    except Exception as e:
        print(f"Błąd podczas połączenia: {e}. ")
    finally:
        engine.dispose()

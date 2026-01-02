import pandas as pd
from pathlib import Path


# wczytywanie danych z csv
def load_names_surenames():
    # Path do pliku
    base_path = Path(__file__).parent
    folder_path = base_path / 'raw_data'

    def read_names_csv(file_name):
        file_path = folder_path / file_name
        return pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')

    try:
        imiona_meskie = read_names_csv('imiona_meskie.csv')
        imiona_zenskie = read_names_csv('imiona_zenskie.csv')
        nazwiska_meskie = read_names_csv('nazwiska_meskie.csv')
        nazwiska_zenskie = read_names_csv('nazwiska_zenskie.csv')

        return imiona_meskie, imiona_zenskie, nazwiska_meskie, nazwiska_zenskie

    except FileNotFoundError as e:
        print(f"Bład : Nie znaleziono pliku")
        return None
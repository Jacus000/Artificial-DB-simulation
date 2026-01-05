import pandas as pd
from pathlib import Path


# data_names nazwy plikow w postaci tablicy stringow
def load_data(data_names):
    # Path do pliku
    base_path = Path(__file__).parent
    folder_path = base_path / 'raw_data'

    def read_names_csv(file_name):
        file_path = folder_path / file_name
        return pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')

    try:
        Data = []
        for file in data_names:
            Data.append(read_names_csv(file))

        return Data

    except FileNotFoundError as e:
        print(f"Bład : Nie znaleziono pliku")
        return None
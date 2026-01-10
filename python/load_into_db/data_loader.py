import pandas as pd
from pathlib import Path


# data_names nazwy plikow w postaci tablicy stringow
def load_data(data_names):
    # Path do pliku
    current_file = Path(__file__).resolve()
    base_project_path = current_file.parents[2]
    folder_path = base_project_path / 'data' / 'raw_data'

    def read_names_csv(file_name):
        file_path = folder_path / file_name
        if not file_path.exists():
            print(f"Blad nie znaleziono pliku {file_path}")
        return pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')

    try:
        data_frames = []
        for file in data_names:
            df = read_names_csv(file)
            if df is not None:
                data_frames.append(df)
        return data_frames

    except FileNotFoundError as e:
        print(f"Bład : Nie znaleziono pliku")
        return None
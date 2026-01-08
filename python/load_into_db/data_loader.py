import pandas as pd
from pathlib import Path


# # data_names nazwy plikow w postaci tablicy stringow
# def load_data(data_names):
#     # Path do pliku
#     base_path = Path(__file__).parent
#     folder_path = base_path / 'raw_data'
#
#     def read_names_csv(file_name):
#         file_path = folder_path / file_name
#         return pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')
#
#     try:
#         Data = []
#         for file in data_names:
#             Data.append(read_names_csv(file))
#
#         return Data
#
#     except FileNotFoundError as e:
#         print(f"Bład : Nie znaleziono pliku")
#         return None

def load_data(file_name: str) -> pd.DataFrame:
    """
    Wczytuje dowolny plik CSV z folderu 'data/raw_data' w głównym katalogu projektu.
    Funkcja sama oblicza ścieżkę względem swojej lokalizacji.
    """
    try:
        # 1. Obliczamy ścieżkę do głównego folderu projektu
        # Zakładamy, że ten skrypt jest w: python/load_into_db/ (czyli 2 poziomy w dół)
        project_root = Path(__file__).resolve().parents[2]

        # 2. Budujemy pełną ścieżkę do konkretnego pliku
        file_path = project_root / 'data' / 'raw_data' / file_name

        # 3. Wczytujemy dane
        # sep=None i engine='python' pozwala na automatyczne wykrycie separatora (, lub ;)
        df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')

        return df

    except FileNotFoundError:
        print(f" BŁĄD: Nie znaleziono pliku: {file_name}")
        print(f" Szukano w: {file_path}")
        return pd.DataFrame()  # Zwracamy puste DataFrame, żeby program się nie wywalił
    except Exception as e:
        print(f" Inny błąd podczas ładowania {file_name}: {e}")
        return pd.DataFrame()



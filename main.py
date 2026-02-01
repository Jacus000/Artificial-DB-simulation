import sys
from python.generation_orchestrator import DataGeneratorOrchestrator 

def main():
    try:
        orchestrator = DataGeneratorOrchestrator()
        orchestrator.run_all()
        print("Success: Database is populated.")
    except Exception as e:
        print(f"Unexpected error in main: {e}")
        sys.exit(1)
#Jak wygenerowac cala baze:
#1. Tworzymy strukture bazy: w folderze projektu odpalamy basha -> cd scripts -> ./init_db.sh -> wpisujemy haslo
#2. Wypelniamy tabele statyczne ./fill_static_data.sh -> wpisujemy haslo (powinnismy je przechowywac w .env)
# WAZNE jezeli mamy strukture i jakies dane ale chcemy je wygenerowac na nowo to uzywamy clean_db.sql -> punkt 2.
#3. Odpalamy python main
#4. Po calym procesie struktura bazy wraz z danymi powinna byc na serwerze
if __name__ == "__main__":
    main()
    
import math
import random as rd
import numpy as np
from datetime import datetime, timezone, timedelta
from db.fetch_from_db import DataBaseAccess
import pandas as pd

class GenerateSalaryHistory:
    def __init__(self, starting_date: datetime):
        self.starting_date = starting_date
        self.db = DataBaseAccess()
        self.now = datetime.now(timezone.utc)

    def probablity_raise(self, worker_lenght_of_service):#w miesiacach
        if worker_lenght_of_service>=24:
            return 0.96
        prob = (worker_lenght_of_service // 2 + 1) * 0.08
        return min(prob,1.0)

    def generate_salary_history(self):
        history_records = []
        try:
            query = """
                SELECT e.id_employee, p.base_salary 
                FROM employees e
                JOIN positions p ON e.id_position = p.id_position
            """
            data = self.db.fetch_all(query)

            if len(data) == 0:
                return pd.DataFrame()
            
            data_list = [(row["id_employee"], row["base_salary"]) for row in data]
            starter_data_ids = {row[0] for row in rd.sample(data_list, int(len(data_list) * 0.7))}

            for emp_id, base_salary in data_list:
                # Ustalenie daty zatrudnienia
                if emp_id in starter_data_ids:
                    hire_date = self.starting_date
                else:
                    random_days = rd.randint(0, max(1, (self.now - self.starting_date).days))
                    hire_date = self.starting_date + timedelta(days=random_days)
                
                current_salary = base_salary
                # record_start_date śledzi, od kiedy obowiązuje OBECNA pensja
                record_start_date = hire_date
                current_date = hire_date

                while current_date < self.now:
                    months = rd.randint(4, 16)
                    next_review_date = current_date + timedelta(days=months * 30)

                    # Sprawdzamy, czy w tym terminie "przeglądu" wpada podwyżka
                    months_of_service = (current_date - self.starting_date).days / 30
                    
                    # Jeśli następuje podwyżka I nie wybiegamy w przyszłość
                    if next_review_date < self.now and rd.random() < self.probablity_raise(months_of_service):
                        # Zamykamy poprzedni rekord pensji
                        history_records.append({
                            "id_employee": emp_id,
                            "base_amount": current_salary,
                            "valid_from": record_start_date,
                            "valid_to": next_review_date
                        })
                        
                        # Naliczamy podwyżkę i ustawiamy nową datę rozpoczęcia dla nowej kwoty
                        raise_percent = rd.uniform(0.05, 0.2)
                        current_salary = round(current_salary * (1 + raise_percent), 2)
                        record_start_date = next_review_date
                    
                    # Przesuwamy czas do przodu niezależnie od podwyżki
                    current_date = next_review_date

                # Na koniec pętli dodajemy "obecnie obowiązującą" pensję (valid_to = None)
                history_records.append({
                    "id_employee": emp_id,
                    "base_amount": current_salary,
                    "valid_from": record_start_date,
                    "valid_to": None
                })

            df_salary = pd.DataFrame(history_records)
            if not df_salary.empty:
                df_salary['valid_from'] = pd.to_datetime(df_salary['valid_from']).dt.date
                df_salary['valid_to'] = pd.to_datetime(df_salary['valid_to']).dt.date
                df_salary = df_salary.where(pd.notnull(df_salary), None)
            return df_salary

        except Exception as e:
            print(f"Błąd: {e}")
            return pd.DataFrame()
        
if __name__ == "__main__":
    starting_date = datetime(2024, 1, 12, tzinfo=timezone.utc)
    generator = GenerateSalaryHistory(starting_date)
    df_results = generator.generate_salary_history()
    
    if not df_results.empty:
        data_to_save = df_results.to_dict(orient='records')
        db = DataBaseAccess()
        db.insert_data("salary_history", data_to_save)
        print("Pomyślnie zapisano dane w bazie.")
        
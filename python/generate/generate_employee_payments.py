import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta, date, timezone
from dateutil.relativedelta import relativedelta
from python.db.fetch_from_db import DataBaseAccess

class GenerateEmployeePayments:
    def __init__(self, **kwargs):
        self.db = DataBaseAccess()

    def generate(self):
        query = "SELECT * FROM salary_history"
        try:
            history_data = self.db.fetch_all(query)
        except Exception as e:
            print(f"Error fetching salary_history: {e}")
            return pd.DataFrame()

        if not history_data:
            print("No salary history found.")
            return pd.DataFrame()

        # Używamy słownika do przechowywania unikalnych wpisów
        # Klucz: (id_employee, data_miesiaca)
        payments_map = {}
        today = date.today()

        for record in history_data:
            id_salary = record['id_salary']
            id_employee = record['id_employee']
            base_amount = float(record['base_amount'])
            
            start_date = record['valid_from']
            if isinstance(start_date, (datetime, pd.Timestamp)):
                start_date = start_date.date()
            
            end_date = record['valid_to']
            if end_date is None:
                end_date = today
            elif isinstance(end_date, (datetime, pd.Timestamp)):
                end_date = end_date.date()

            current_month_date = start_date.replace(day=1)
            
            while current_month_date <= end_date:
                #tworzymy unikalny klucz dla pary pracownik dany miesiac
                key = (id_employee, current_month_date)
                
                next_month = current_month_date + relativedelta(months=1)
                payment_date = next_month.replace(day=10)

                bonus = 0.0
                if random.random() < 0.20:
                    mean_bonus = base_amount * 0.05
                    bonus = round(random.expovariate(1 / mean_bonus), 2) if mean_bonus > 0 else 0.0

                deduction = 0.0
                if random.random() < 0.20:
                    mean_dedu = base_amount * 0.02
                    deduction = round(random.expovariate(1 / mean_dedu), 2) if mean_dedu > 0 else 0.0

                if deduction > base_amount + bonus:
                    deduction = base_amount + bonus 

                payments_map[key] = {
                    "id_employee": id_employee,
                    "salary_month": current_month_date,
                    "base_salary_id": id_salary,
                    "bonus": bonus,
                    "deduction": deduction,
                    "payment_date": payment_date,
                }

                current_month_date += relativedelta(months=1)

        final_payments = list(payments_map.values())
        final_payments.sort(key=lambda x: (x['salary_month'], x['id_employee']))
        df = pd.DataFrame(final_payments)
        data_to_send = df.to_dict(orient='records')

        return data_to_send

# if __name__ == "__main__":
#     gen = GenerateEmployeePayments()
#     df = gen.generate()
#     if not df.empty:
#         print(f"Generated {len(df)} payments.")
#         data_to_save = df.to_dict(orient="records")
#         db = DataBaseAccess()
#         db.insert_data("employee_payments", data_to_save)


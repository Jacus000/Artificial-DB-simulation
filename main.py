from python.generate.generate_employees import GenerateEmployees
from python.generate.generate_salary_history import GenerateSalaryHistory
from datetime import timezone, datetime
import pandas as pd
from python.db.fetch_from_db import DataBaseAccess

def main():
    starting_date = datetime(2024, 1, 12, tzinfo=timezone.utc)
    genemp = GenerateEmployees(150)
    gensalary = GenerateSalaryHistory(starting_date)
    employees = genemp.generate_staff()
    employees_salary = gensalary.generate_salary_history()
    generators = {
        "employees": employees,
        "salary_history": employees_salary
    }
    db = DataBaseAccess()

    for id, value in enumerate(generators):
        if not value.empty:
            data_to_save = value.to_dict(orient='records')
            db.insert_data(id, data_to_save)
            print(f"Pomyślnie zapisano plik {id} w bazie")

if __name__ == "__main__":
    main()
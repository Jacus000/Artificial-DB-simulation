from python.generate.generate_employee_payments import GenerateEmployeePayments
from python.generate.generate_employees import GenerateEmployees
from python.generate.generate_employees_personal_data import GenerateEmployeesPersonalData
from python.generate.generate_salary_history import GenerateSalaryHistory

from python.db.fetch_from_db import DataBaseAccess

from datetime import datetime, timezone

DB_CONFIG = {
    "employees_count": 150,
    "starting_date": datetime(2024, 1, 12, tzinfo=timezone.utc),
}

class DataGeneratorOrchestrator:
    def __init__(self):
        self.db_acess = DataBaseAccess()
        self.pipeline = [
            (GenerateEmployees, "employees"),
            (GenerateEmployeesPersonalData, "employee_personal_data"),
            (GenerateSalaryHistory, "salary_history"),
            (GenerateEmployeePayments, "employee_payments")
        ]
    def run_all(self):
        print("DB data generation process started")
        for generator_class, name in self.pipeline:
            try:
                print(f"Generating {name} table")
                generator = generator_class(**DB_CONFIG)
                result = generator.generate()

                if result is None or (isinstance(result, list) and not result):
                    print(f"No data generated for {name}")
                    continue

                self.db_acess.insert_data(name, result)
                print(f"{name} generation and insert ended with succes")
    
            except Exception as e:
                print(f"Process failed with: {e}")
                break
                

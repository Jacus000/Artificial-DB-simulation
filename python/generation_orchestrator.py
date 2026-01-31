from python.generate.generate_employee_payments import GenerateEmployeePayments
from python.generate.generate_employees import GenerateEmployees
from python.generate.generate_employees_personal_data import GenerateEmployeesPersonalData
from python.generate.generate_salary_history import GenerateSalaryHistory
from python.generate.generate_facility_expenses import GenerateFacilityExpenses
from python.generate.generate_facility_sales import GenerateFacilitySales
from python.generate.generate_inspections import GenerateInspections
from python.generate.generate_guest import GenerateGuest
from python.generate.generate_guests_personal_data import GenerateGuestsPersonalData
from python.generate.generate_guests_visit import GenerateGuestsVisits
from python.generate.generate_accidents import GenerateAccidents
from python.generate.generate_compensation_paid import GenerateCompensation
from python.generate.generate_malfunctions import GenerateMalfunctions
from python.generate.generate_attractions_cost import GenerateAttractionCosts

from python.generate.generate_attraction_visits import GenerateAttractionVisits

from python.db.fetch_from_db import DataBaseAccess

from datetime import datetime, timezone
import os
import subprocess
from pathlib import Path

DB_CONFIG = {
    "employees_count": 150,
    "guest_count": 2000,
    "max_number_of_rides_per_entry": 6, #ostroznie wiecej moze wysadzic czas oczekiwania (mozna zmienic ilosc gosci), minimum 3
    "daily_guests": 600,
    "todays_date": datetime.now(timezone.utc),
    "starting_date": datetime(2024, 1, 12, tzinfo=timezone.utc),
    "intensity": 0.8, #expenses/sales intensity
    "probability_of_accidents": 0.001 #0.001 bardzo malo
}

class DataGeneratorOrchestrator:
    def __init__(self):
        self.db_acess = DataBaseAccess()
        self.pipeline = [#kolejnosc jest wazna
            (GenerateEmployees, "employees"),
            (GenerateEmployeesPersonalData, "employee_personal_data"),
            (GenerateSalaryHistory, "salary_history"),
            (GenerateEmployeePayments, "employee_payments"),
            (GenerateFacilityExpenses, "facility_expenses"),
            (GenerateFacilitySales, "facility_sales"),
            (GenerateInspections, "inspections"),
            (GenerateGuest, "guest"),
            (GenerateGuestsPersonalData, "guests_personal_data"),
            (GenerateGuestsVisits, "guests_visit"),
            (GenerateAccidents, "accidents"),
            (GenerateCompensation, "compensation_paid"),
            (GenerateMalfunctions, "malfunction_report"),
            (GenerateAttractionCosts, "attraction_costs"),
            (GenerateAttractionVisits, "attraction_visits")
        ]

        #self.sql_clean_up_path = "database/seeds/dev/clean_db.sql"
        #self.static_columns = "bash scripts/fill_static_data.sh"
    def run_all(self):
        #self._cleanup_db()
        #self._populate_static_data()

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
    def _cleanup_db(self):
        if not os.path.exists(self.sql_clean_up_path):
            print("Couldnt find cleanup script path")
            return
        with open(self.sql_clean_up_path, "r", encoding='utf-8') as file:
            sql_commands = file.read()
        self.db_acess.execute(sql_commands)
    
    def _populate_static_data(self):
        if not os.path.exists(self.static_columns):
            print("Couldnt find cleanup script path")
            return
        try:
            result = subprocess.run(['bash', self.static_columns], check=True, capture_output=True, text=True)
            print("static tables created")
        except subprocess.CalledProcessError as e:
            print(f"Shell script failed with error: {e.stderr}")
            raise



                

import random
import pandas as pd
from datetime import datetime, timedelta, timezone
from python.db.fetch_from_db import DataBaseAccess

class GenerateInspections:
    def __init__(self, starting_date: datetime, **kwargs):
        self.db = DataBaseAccess()
        self.now = datetime.now(timezone.utc).replace(tzinfo=None)
        self.start_date = starting_date.replace(tzinfo=None)

    def generate(self):
        query_employees = "SELECT id_employee FROM employees WHERE id_position IN (4, 5, 6, 7, 8)"
        query_attractions = "SELECT id_attraction FROM attractions"
        
        try:
            employees = self.db.fetch_all(query_employees)
            attractions = self.db.fetch_all(query_attractions)

            if not employees or not attractions:
                print("Workers or attractions not found")
                return None

            technicians = [e['id_employee'] for e in employees]
            all_inspections = []

            for attr in attractions:
                attr_id = attr['id_attraction']
            
                current_date = self.start_date + timedelta(days=random.randint(0, 7))
                #symulacja ciagnacych sie problemow
                last_failed = False

                while current_date < self.now:
                    inspector_id = random.choice(technicians)
                    
                    if last_failed:
                        result = random.choices(['passed', 'failed'], weights=[40, 60])[0]
                    else:
                        result = random.choices(['passed', 'failed'], weights=[95, 5])[0]

                    #data nastepnej inspekcji
                    gap = random.randint(14, 30)
                    next_date = current_date + timedelta(days=gap)

                    all_inspections.append({
                        "id_attraction": attr_id,
                        "id_employee": inspector_id,
                        "inspection_date": current_date,
                        "next_inspection_date": next_date,
                        "result": result
                    })

                    last_failed = (result == 'failed')
                    
                    current_date = next_date

            if not all_inspections:
                return None
            df = pd.DataFrame(all_inspections)
            
            df["inspection_date"] = pd.to_datetime(df["inspection_date"]).dt.date
            df["next_inspection_date"] = pd.to_datetime(df["next_inspection_date"]).dt.date
            
            df = df.sample(frac=1)
            df_sorted = df.sort_values(by='inspection_date')

            return df_sorted.to_dict(orient='records')

        except Exception as e:
            print(f"Error while generating inspections: {e}")
            raise

# if __name__ == "__main__":
#     start = datetime(2024, 1, 12, tzinfo=timezone.utc)
#     generator = GenerateInspections(start)
#     result = generator.generate()
#     print(result)
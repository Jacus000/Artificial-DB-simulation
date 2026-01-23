
import random
import math
from .generate_filler import names_surenames_generator
from db.fetch_from_db import DataBaseAccess

class GenerateEmployees:
    def __init__(self, employees_count: int):
        self.employees_count = employees_count
        self.db = DataBaseAccess()

    def generate_staff(self):
        
        employees_df = names_surenames_generator(self.employees_count)
        employees_df["id_position"] = None
        
        try:
            positions = self.db.fetch_all("SELECT id_position, base_salary FROM positions")
            positions_list = [(row["id_position"], row["base_salary"]) for row in positions]

            position_ids = [p[0] for p in positions_list]
            salaries = [p[1] for p in positions_list]
            
            alpha = 0.00012
            weights = [math.exp(-alpha*s) for s in salaries]
            
            idx = 0
            for posid in position_ids:
                if idx >= self.employees_count:
                    break
                employees_df.loc[idx, "id_position"] = posid
                idx+=1
            
            for i in range(idx, self.employees_count):
                chosen_id = random.choices(position_ids, weights=weights, k=1)[0]
                employees_df.loc[i, "id_position"] = chosen_id
            
            employees_df = employees_df.sample(frac=1)

            return employees_df

        except Exception as e:
            print(f"Błąd połączenia: {e}")
            return []

if __name__ == "__main__":
    employee = GenerateEmployees(100).generate_staff()
    if not employee.empty:
        data_to_save = employee.to_dict(orient = 'records')
        db = DataBaseAccess()
        db.insert_data("employees", data_to_save)
    else:
        print("brak danych do zapisania")
    #print(employee)






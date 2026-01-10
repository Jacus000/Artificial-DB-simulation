from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import random
import math
from dotenv import load_dotenv
import os
from .generate_filler import names_surenames_generator

# Format: mariadb+mariadbconnector://uzytkownik:haslo@host:port/nazwa_bazy

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_NAME")


engine = create_engine(f"mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

class GenerateEmployees:
    def __init__(self, employees_count: int):
        self.employees_count = employees_count

    def generate_staff(self):
        positions_list = []
        
        employees_df = names_surenames_generator(self.employees_count)
        employees_df["id_position"] = None
        
        try:
            with engine.connect() as connection:
                query = text("SELECT id_position, base_salary FROM positions")
                #query2 = text("SELECT COUNT(*) FROM employees")
                result = connection.execute(query)
                #count = connection.execute(query2).scalar_one()
                
                for row in result.mappings():
                    positions_list.append(
                          (row["id_position"], row["base_salary"])
                    )
            
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
            return [], 0
    
employee = GenerateEmployees(100).generate_staff()
print(employee)





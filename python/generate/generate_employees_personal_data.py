import pandas as pd
from python.db.fetch_from_db import DataBaseAccess
from .generate_filler import pesel_generator, email_generator, address_generator2, phone_number_generator

class GenerateEmployeesPersonalData:
    def __init__(self, **kwargs):
        self.db = DataBaseAccess()

    def generate(self):
        query = "SELECT id_employee, first_name, last_name, gender FROM employees"
        try:
            employees = self.db.fetch_all(query)
        except Exception as e:
            print(f"Error fetching employees: {e}")
            return pd.DataFrame()
        
        if not employees:
            print("No employees found in DB.")
            return pd.DataFrame()
            
        df = pd.DataFrame(employees)
        df['name'] = df['first_name']

        df = email_generator(df)
        
        count = len(df)
        phones = phone_number_generator(count)
        df['phone_number'] = phones['phone_number'].values
        
        addresses = address_generator2(count)
        
        df['adress'] = addresses['ulica'] + " " + addresses['numer_domu'].astype(str)
        df['postal_code'] = addresses['kod_pocztowy']
        df['city'] = addresses['miasto']
        
        df['temp_gender'] = df['gender'].map({'man': 'Male', 'woman': 'Female'})

        original_gender = df['gender']
        df['gender'] = df['temp_gender']
        
        df = pesel_generator(df)
        
        df['gender'] = original_gender
        
        final_df = df[['id_employee', 'adress', 'postal_code', 'city', 'phone_number', 'PESEL', 'email']]
        
        data_to_send = final_df.to_dict(orient='records')
        return data_to_send

# if __name__ == "__main__":
#     gen = GenerateEmployeesPersonalData()
#     df = gen.generate()
#     if not df.empty:
#         db = DataBaseAccess()
#         db.insert_data("employee_personal_data", df.to_dict(orient='records'))
#         print("Inserted employee personal data.")
#     else:
#         print("No data generated.")

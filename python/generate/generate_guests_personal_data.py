import pandas as pd
from python.db.fetch_from_db import DataBaseAccess
from .generate_filler import pesel_generator, email_generator, address_generator2, phone_number_generator
import random
import numpy as np

class GenerateGuestsPersonalData:
    def __init__(self, **kwargs):
        self.db = DataBaseAccess()

    def generate(self):
        query = "SELECT id_guest, first_name, last_name, gender FROM guest"
        try:
            guests = self.db.fetch_all(query)
        except Exception as e:
            print(f"Error fetching guests: {e}")
            return pd.DataFrame()
        
        if not guests:
            print("No guests found in DB.")
            return pd.DataFrame()
            
        df = pd.DataFrame(guests)
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

        df['age'] = 2026 - df['PESEL'].astype(str).str[:2].astype(int).apply(lambda x: 1900 + x if x > 20 else 2000 + x)
        
        def generate_height(row):
            age = row['age']
            gender = row['gender']
            
            if age < 18:
                if age < 5:
                    base_height = 80 + (age * 6)
                    variation = random.randint(-5, 5)
                elif age < 12:
                    base_height = 110 + ((age - 5) * 5)
                    variation = random.randint(-8, 8)
                else:
                    base_height = 145 + ((age - 12) * 4)
                    variation = random.randint(-10, 10)
            else:
                if gender == 'Male': # Man
                    base_height = 180
                    variation = int(np.random.normal(0, 7))
                else: # Woman
                    base_height = 165
                    variation = int(np.random.normal(0, 6))
            
            return max(50, min(220, base_height + variation))
        
        df['height'] = df.apply(generate_height, axis=1)
        
        df['gender'] = original_gender
        
        final_df = df[['id_guest', 'phone_number', 'height', 'email' ,'PESEL', 'city']]
        
        data_to_send = final_df.to_dict(orient='records')
        return data_to_send

# if __name__ == "__main__":
#     gen = GenerateGuestsPersonalData
#     df = gen.generate()
#     print(df)

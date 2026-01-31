import random
from datetime import timedelta, timezone, datetime
from python.db.fetch_from_db import DataBaseAccess
import pandas as pd

class GenerateAccidents:
    def __init__(self, starting_date, todays_date, probability_of_accidents: float, **kwargs):
        self.starting_date = starting_date
        self.now = todays_date
        self.acc_prob = probability_of_accidents
        self.db = DataBaseAccess()

    def generate(self):
        attractions = self.db.fetch_all("SELECT id_attraction, is_vr_capable FROM attractions")
        acc_types = self.db.fetch_all("SELECT id_accident_type, accident_type_name, suggest_compensation FROM accident_type")
        visits = self.db.fetch_all("SELECT id_visit, visit_date FROM guests_visit")

        accidents_to_insert = []

        vr_accident = next(t for t in acc_types if t['accident_type_name'] == 'VR Disorientation Injury')
        fatal_accident = next(t for t in acc_types if t['accident_type_name'] == 'Fatal Accident')
        
        for visit in visits:
            if random.random() < self.acc_prob:
                attraction = random.choice(attractions)
                
                available_types = [
                    t for t in acc_types 
                    if t['accident_type_name'] != 'VR Disorientation Injury' or attraction['is_vr_capable']
                ]
                #zmniejszamy prob wypadku smiertelnego
                weights = []
                for t in available_types:
                    if t['accident_type_name'] in ['Minor Injury', 'Fall on Park Area']:
                        weights.append(5.0)
                    elif t['accident_type_name'] == 'Fatal Accident':
                        weights.append(0.01)
                    else:
                        weights.append(1.0)

                chosen_type = random.choices(available_types, weights=weights)[0]

                accident_data = {
                    'id_visit': visit['id_visit'],
                    'id_attraction': attraction['id_attraction'],
                    'id_accident_type': chosen_type['id_accident_type'],
                    'accident_description': f"Incident involving {chosen_type['accident_type_name']} at attraction ID {attraction['id_attraction']}",
                    'report_date': visit['visit_date']
                }
                
                accidents_to_insert.append(accident_data)
        data_to_load = pd.DataFrame(accidents_to_insert)
        return data_to_load.to_dict(orient='records')
    
if __name__ == "__main__":
    gen = GenerateAccidents(datetime(2024, 1, 12, tzinfo=timezone.utc), datetime.now(), 0.001)
    result = gen.generate()
    print(result)
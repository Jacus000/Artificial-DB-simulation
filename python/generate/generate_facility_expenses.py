from python.db.fetch_from_db import DataBaseAccess
import random
from datetime import datetime, timedelta, timezone
import pandas as pd

class GenerateFacilityExpenses:
    CONFIG = {#format (typ wydatku) : (czestosc, (sredni koszt))
        'restaurant': {
            'FoodAndBeverages': (70, (200, 1500)),
            'AlcoholSupplies':  (15, (500, 2500)),
            'Utilities':        (5,  (1000, 4000)),
            'Cleaning':         (10, (100, 500))
        },
        'bar': {
            'AlcoholSupplies':  (60, (300, 2000)),
            'FoodAndBeverages': (20, (100, 500)),
            'Utilities':        (10, (800, 2500)),
            'Security':         (10, (200, 600))
        },
        'casino': {
            'Security':            (40, (2000, 10000)),
            'LicensingAndPermits': (5,  (5000, 20000)),
            'AlcoholSupplies':     (30, (1000, 5000)),
            'Utilities':           (25, (3000, 15000))
        },
        'photo_booth': {
            'PhotoMaterials': (80, (20, 100)),
            'Maintenance':    (10, (100, 300)),
            'Utilities':      (10, (50, 150))
        },
        'souvenir_shop': {
            'Merchandise': (60, (500, 2500)),
            'Utilities':   (20, (200, 1000)),
            'Cleaning':    (20, (50, 200))
        }
    }
    def __init__(self, starting_date: datetime, intensity: float, **kwargs):
        self.db = DataBaseAccess()
        self.now = datetime.now(timezone.utc)
        self.start_date = starting_date
        self.intensity = intensity

    def generate(self):
        query = "SELECT id_facility, facility_type FROM facilities"
        try:
            facilities = self.db.fetch_all(query)
            all_expenses = []
            num_days = (self.now - self.start_date).days
            for f in facilities:
                f_id = f["id_facility"]
                f_type = f["facility_type"]

                settings = self.CONFIG[f_type]
                categories = list(settings.keys())
                weights = [w[0] for w in settings.values()]

                for day in range(num_days):
                    current_date = self.now - timedelta(days=day)
                    number_of_transaction = random.randint(0, int(3*self.intensity))

                    for _ in range(number_of_transaction):
                        category = random.choices(categories, weights=weights)[0]
                        price_range = settings[category][1]
                        cost = self._get_authentic_cost(price_range)

                        timestamp = current_date.replace(
                            hour=random.randint(10, 20), 
                            minute=random.randint(0, 59)
                        )

                        all_expenses.append({
                            "expense_date": timestamp,
                            "expense_cost": cost,
                            "id_facility": f_id,
                            "expense_category": category
                        })

            final_result = pd.DataFrame(all_expenses)
            
            final_result = final_result.sample(frac=1)

            final_result["expense_date"] = pd.to_datetime(final_result["expense_date"])
            final_result["expense_date"] = final_result["expense_date"].dt.tz_localize(None)
            final_result["expense_date"] = final_result["expense_date"].dt.floor('s')

            final_sorted = final_result.sort_values(by='expense_date')

            data_to_send = final_sorted.to_dict(orient='records')
            return data_to_send
                
        except Exception as e:
            print(f"Theres an error while generating {e}")
            return None
    
    def _get_authentic_cost(self, price_range):
        low, high = price_range
        mu = low + (high - low) * 0.4
        sigma = (high - low) / 6 
        cost = random.gauss(mu, sigma)
        cost = max(low, min(high, cost))
        return round(cost, 2)
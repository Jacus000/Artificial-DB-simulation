import random
import pandas as pd
from datetime import datetime, timedelta, timezone
from python.db.fetch_from_db import DataBaseAccess

class GenerateFacilitySales:
    # Konfiguracja sprzedaży: (średnia liczba transakcji dziennie, (min_cena, max_cena))
    # ogolnie przy tych parametrach wygeneruje nam to 600k wynikow. Mozna zmiejszyc ich ilosc manipulujac daily_count
    CONFIG = {
        'restaurant': {
            'daily_count': (20, 50), 
            'price_range': (40.0, 350.0),
            'payments': ['Card', 'Cash', 'BLIK', 'Gift_card'],
            'weights': [50, 20, 25, 5]
        },
        'bar': {
            'daily_count': (30, 90),
            'price_range': (15.0, 120.0),
            'payments': ['Card', 'Cash', 'BLIK'],
            'weights': [60, 25, 15]
        },
        'casino': {
            'daily_count': (10, 20),
            'price_range': (100.0, 5000.0),
            'payments': ['Card', 'Cash', 'BLIK'],
            'weights': [40, 50, 10]
        },
        'photo_booth': {
            'daily_count': (5, 25),
            'price_range': (20.0, 50.0),
            'payments': ['Card', 'BLIK'],
            'weights': [70, 30]
        },
        'souvenir_shop': {
            'daily_count': (20, 40),
            'price_range': (10.0, 250.0),
            'payments': ['Card', 'Cash', 'BLIK', 'Gift_card'],
            'weights': [55, 15, 20, 10]
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
            if not facilities:
                return None

            all_sales = []
            num_days = (self.now - self.start_date).days

            for f in facilities:
                f_id = f["id_facility"]
                f_type = f["facility_type"]
                conf = self.CONFIG[f_type]

                for day in range(num_days):
                    current_date = self.now - timedelta(days=day)
                    
                    #skalujemy parametr przez intensity parametr
                    min_t, max_t = conf['daily_count']
                    count = random.randint(int(min_t * self.intensity), int(max_t * self.intensity))

                    for _ in range(count):
                        amount = self._get_authentic_amount(conf['price_range'])
                        method = random.choices(conf['payments'], weights=conf['weights'])[0]
                        
                        timestamp = current_date.replace(
                            hour=random.randint(10, 20),
                            minute=random.randint(0, 59),
                            second=random.randint(0, 59),
                            microsecond=0
                        )

                        all_sales.append({
                            "sale_date": timestamp,
                            "total_amount": amount,
                            "id_facility": f_id,
                            "payment_method": method
                        })

            if not all_sales:
                return None

            df = pd.DataFrame(all_sales)
            df["sale_date"] = pd.to_datetime(df["sale_date"]).dt.tz_localize(None)
            df = df.sample(frac=1)
            
            return df.sort_values(by='sale_date').to_dict(orient='records')

        except Exception as e:
            print(f"Error in sales generation: {e}")
            raise

    def _get_authentic_amount(self, p_range):
        low, high = p_range
        mu = low + (high - low) * 0.2
        sigma = (high - low) / 4
        val = random.gauss(mu, sigma)
        return round(max(low, min(high, val)), 2)
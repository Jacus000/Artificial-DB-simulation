import random
from datetime import timedelta, datetime, date
import pandas as pd
from python.db.fetch_from_db import DataBaseAccess

class GenerateAttractionCosts:
    def __init__(self, starting_date: datetime, todays_date: datetime, **kwargs):
        self.db = DataBaseAccess()
        self.starting_date = starting_date.replace(tzinfo=None)
        self.now = todays_date.replace(tzinfo=None)

    def generate(self):
        attractions = self.db.fetch_all("SELECT id_attraction, att_name, att_type FROM attractions")
        malfunctions = self.db.fetch_all("""
            SELECT id_malfunction_report, id_attraction, report_date, priority 
            FROM malfunction_report 
            WHERE is_resolved = 1
        """)
        
        if not attractions:
            return []

        costs_to_insert = []

        current_date = self.starting_date
        first_iteration = True

        while current_date <= self.now:
            for attr in attractions:
                profile = self._get_profile(attr['att_type'])
                
                costs_to_insert.append({
                    'id_attraction': attr['id_attraction'],
                    'cost_type': 'power',
                    'amount': round(random.uniform(profile['power_min'], profile['power_max']), 2),
                    'cost_date': current_date.date(),
                    'id_malfunction': None
                })
                
                costs_to_insert.append({
                    'id_attraction': attr['id_attraction'],
                    'cost_type': 'maintenance',
                    'amount': round(random.uniform(profile['maint_min'], profile['maint_max']), 2),
                    'cost_date': current_date.date(),
                    'id_malfunction': None
                })
            
            if first_iteration:
                month = current_date.month + 1
                year = current_date.year
                if month > 12:
                    month = 1
                    year += 1
                current_date = datetime(year, month, 1)
                first_iteration = False
            else:
                month = current_date.month + 1
                year = current_date.year
                if month > 12:
                    month = 1
                    year += 1
                current_date = datetime(year, month, 1)

        for malf in malfunctions:
            prio_map = { # tutaj tez mozna zmieniac koszty
                'low': random.uniform(200, 1000),
                'medium': random.uniform(1000, 3500),
                'high': random.uniform(3500, 12000),
                'critical': random.uniform(12000, 60000)
            }
            

            cost_dt = malf['report_date']

            costs_to_insert.append({
                'id_attraction': malf['id_attraction'],
                'cost_type': 'repair',
                'amount': round(prio_map.get(malf['priority'], 1500.0), 2),
                'cost_date': cost_dt.date(),
                'id_malfunction': malf['id_malfunction_report']
            })

        df = pd.DataFrame(costs_to_insert)
        if not df.empty:
            df['id_malfunction'] = df['id_malfunction'].astype(object).where(df['id_malfunction'].notnull(), None)
        df = df.sample(frac=1)

        return df.sort_values(by='cost_date').to_dict(orient='records')

    def _get_profile(self, att_type):# mozna pozmieniac te koszty
        profiles = {
            'roller_coaster': {'power_min': 6000, 'power_max': 18000, 'maint_min': 3000, 'maint_max': 7000},
            'thrill_ride':    {'power_min': 3500, 'power_max': 9000,  'maint_min': 1500, 'maint_max': 4000},
            'water_ride':     {'power_min': 4500, 'power_max': 11000, 'maint_min': 1200, 'maint_max': 3500},
            'vr_ride':        {'power_min': 1200, 'power_max': 3500,  'maint_min': 2500, 'maint_max': 6500},
            'family_ride':    {'power_min': 600,  'power_max': 2500,  'maint_min': 600,  'maint_max': 2000},
            'ferris_wheel':   {'power_min': 1200, 'power_max': 4000,  'maint_min': 1000, 'maint_max': 2500},
            'kids_ride':      {'power_min': 300,  'power_max': 1000,  'maint_min': 400,  'maint_max': 1200},
            'dark_ride':      {'power_min': 2500, 'power_max': 6000,  'maint_min': 1500, 'maint_max': 3500}
        }
        return profiles[att_type]
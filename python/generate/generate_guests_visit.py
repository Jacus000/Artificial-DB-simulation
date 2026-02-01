import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta, timezone
from python.db.fetch_from_db import DataBaseAccess

class GenerateGuestsVisits:
    def __init__(self, starting_date: datetime, **kwargs):
        self.db = DataBaseAccess()
        self.starting_date = starting_date.replace(tzinfo=None)
        self.now = datetime.now()

    def calculate_age(self, pesels):
        pesels = pesels.astype(str)
        years = pesels.str[:2].astype(int)
        months = pesels.str[2:4].astype(int)
        
        full_years = np.where(months > 20, 2000 + years, 1900 + years)
        return 2026 - full_years

    def generate(self):
        guests_data = self.db.fetch_all("SELECT g.id_guest, gp.pesel FROM guest g JOIN guests_personal_data gp ON g.id_guest = gp.id_guest")
        tickets_data = self.db.fetch_all("SELECT id_ticket_type, ticket_type_name, price FROM ticket_types")
        total_guests = self.db.fetch_scalar("SELECT count(*) FROM guest")
        
        if not guests_data or not tickets_data:
            return []

        df_guests = pd.DataFrame(guests_data)
        df_tickets = pd.DataFrame(tickets_data)
        
        df_guests['age'] = self.calculate_age(df_guests['pesel'])
        
        categories = {
            'child': ['Children Ticket', 'VR access pass', 'Double Safety Ticket', 'Double Safety + Foodie Ticket'],
            'senior': ['Senior Ticket', 'Normal Ticket', 'VIP ticket', 'VR access pass', 'Double Safety + Foodie Ticket'],
            'student': None,
            'adult': None    
        }

        ticket_pools = {}
        for cat, names in categories.items():
            if cat == 'child':
                mask = df_tickets['ticket_type_name'].isin(names)
            elif cat == 'senior':
                mask = df_tickets['ticket_type_name'].isin(names)
            elif cat == 'student':
                mask = ~df_tickets['ticket_type_name'].isin(['Children Ticket', 'Senior Ticket'])
            else:
                mask = ~df_tickets['ticket_type_name'].isin(['Children Ticket', 'Senior Ticket', 'Student Ticket', 'VR access pass', 'Double Safety + Foodie Ticket'])
            
            sub_df = df_tickets[mask]
            w = 1 / sub_df['price'].astype(float)
            probs = w / w.sum()
            ticket_pools[cat] = {
                'ids': sub_df['id_ticket_type'].values,
                'probs': probs.values
            }

        all_visits = []
        days_diff = (self.now - self.starting_date).days
        
        #mozna pozmienia
        max_g = int(total_guests / 65)
        min_g = int(max_g / 2)

        for i in range(days_diff + 1):
            day_date = self.starting_date + timedelta(days=i)
            
            #logika sezonowosci

            if 4 <= day_date.month <= 10:
                season_multiplier = 1.0
            else:
                season_multiplier = 0.5
            
            if day_date.weekday() >= 5:
                season_multiplier *= 1.2

            current_min = max(1, int(min_g * season_multiplier))
            current_max = max(2, int(max_g * season_multiplier))
            num_guests_today = random.randint(current_min, current_max)
            
            if num_guests_today > len(df_guests):
                num_guests_today = len(df_guests)
                
            todays_df = df_guests.sample(n=num_guests_today, replace=False).copy()
            
            todays_df['cat'] = np.select(
                [todays_df['age'] < 18, todays_df['age'] >= 65, (todays_df['age'] >= 18) & (todays_df['age'] <= 26)],
                ['child', 'senior', 'student'],
                default='adult'
            )

            for cat, group in todays_df.groupby('cat'):
                n_in_cat = len(group)
                pool = ticket_pools[cat]
                chosen_tickets = np.random.choice(pool['ids'], size=n_in_cat, p=pool['probs'])
                
                hours = np.random.randint(10, 20, size=n_in_cat)
                minutes = np.random.randint(0, 60, size=n_in_cat)
                seconds = np.random.randint(0, 60, size=n_in_cat)
                
                for idx, (guest_id, ticket_id) in enumerate(zip(group['id_guest'], chosen_tickets)):
                    visit_time = day_date.replace(hour=hours[idx], minute=minutes[idx], second=seconds[idx], tzinfo=None)
                    all_visits.append({
                        'id_guest': guest_id,
                        'id_ticket_type': ticket_id,
                        'visit_date': visit_time
                    })

        return all_visits

# if __name__ == "__main__":
#     gen = GenerateGuestsVisits(datetime(2024, 1, 12, tzinfo=timezone.utc))
#     results = gen.generate()
#     print(f"{len(results)}")
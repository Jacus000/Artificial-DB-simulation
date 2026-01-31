import pandas as pd
import numpy as np
import random
from datetime import timedelta
from python.db.fetch_from_db import DataBaseAccess

class GenerateAttractionVisits:
    def __init__(self, max_number_of_rides_per_entry: int, **kwargs):
        self.db = DataBaseAccess()
        self.max_rides = max_number_of_rides_per_entry

    def generate(self):
        visits_query = """
            SELECT gv.id_visit, gv.id_guest, gv.visit_date, gpd.height, tt.ticket_type_name 
            FROM guests_visit gv
            JOIN guests_personal_data gpd ON gv.id_guest = gpd.id_guest
            JOIN ticket_types tt ON gv.id_ticket_type = tt.id_ticket_type
        """
        raw_visits = self.db.fetch_all(visits_query)
        if not raw_visits:
            return []
        
        visits_df = pd.DataFrame(raw_visits)
        visits_df['visit_date'] = pd.to_datetime(visits_df['visit_date'])
        visits_df['height'] = visits_df['height'].fillna(170)

        attractions_query = "SELECT id_attraction, height_limit_cm, is_vr_capable FROM attractions"
        attractions_df = pd.DataFrame(self.db.fetch_all(attractions_query))
        attractions_df['height_limit_cm'] = attractions_df['height_limit_cm'].fillna(0)

        malfunctions_query = """
            SELECT id_attraction, report_date, is_resolved_at 
            FROM malfunction_report 
            WHERE is_resolved = 1
        """
        malf_df = pd.DataFrame(self.db.fetch_all(malfunctions_query))
        if not malf_df.empty:
            malf_df['report_date'] = pd.to_datetime(malf_df['report_date'])
            malf_df['is_resolved_at'] = pd.to_datetime(malf_df['is_resolved_at'])

        unique_limits = sorted(attractions_df['height_limit_cm'].unique())
        
        attr_map = {
            'full_access': {
                limit: attractions_df[attractions_df['height_limit_cm'] <= limit]['id_attraction'].tolist()
                for limit in unique_limits
            },
            'no_vr': {
                limit: attractions_df[(attractions_df['height_limit_cm'] <= limit) & (attractions_df['is_vr_capable'] == 0)]['id_attraction'].tolist()
                for limit in unique_limits
            },
            'vr_only': {
                limit: attractions_df[(attractions_df['height_limit_cm'] <= limit) & (attractions_df['is_vr_capable'] == 1)]['id_attraction'].tolist()
                for limit in unique_limits
            }
        }

        visits_df['num_rides'] = np.random.randint(3, self.max_rides + 1, size=len(visits_df))
        rides_df = visits_df.loc[visits_df.index.repeat(visits_df['num_rides'])].copy()

        def get_smart_attraction(row):
            h = row['height']
            ticket = row['ticket_type_name']
            
            if ticket == 'VR access pass':
                pool_type = 'vr_only'
            elif ticket == 'VIP ticket':
                pool_type = 'full_access'
            else:
                pool_type = 'no_vr'
                
            valid_limit = max([l for l in unique_limits if l <= h] + [0])
            pool = attr_map[pool_type][valid_limit]
            
            return random.choice(pool) if pool else None

        rides_df['id_attraction'] = rides_df.apply(get_smart_attraction, axis=1)
        rides_df = rides_df.dropna(subset=['id_attraction'])

        rides_df['visit_time'] = rides_df['visit_date'] + pd.to_timedelta(
            np.random.randint(15, 241, size=len(rides_df)), unit='m'
        )

        if not malf_df.empty:
            merged = pd.merge(rides_df, malf_df, on='id_attraction', how='left')
            
            is_broken = (
                (merged['report_date'].notnull()) & 
                (merged['visit_time'] >= merged['report_date']) & 
                (merged['visit_time'] <= merged['is_resolved_at'])
            )
            
            final_df = merged[~is_broken].drop_duplicates(
                subset=['id_visit', 'id_attraction', 'visit_time']
            )
        else:
            final_df = rides_df

        return final_df[['id_visit', 'id_attraction', 'visit_time']].to_dict(orient='records')
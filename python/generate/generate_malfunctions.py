import random
from datetime import timedelta, datetime, date
import pandas as pd
import numpy as np
from python.db.fetch_from_db import DataBaseAccess

class GenerateMalfunctions:
    def __init__(self, **kwargs):
        self.db = DataBaseAccess()

    def generate(self):
        query = "SELECT id_attraction, id_employee, inspection_date, result FROM inspections"
        all_inspections = self.db.fetch_all(query)
        all_employees = self.db.fetch_all("SELECT id_employee FROM employees")
        
        if not all_inspections:
            return []

        malfunctions_to_insert = []

        # failed inspections
        for insp in all_inspections:
            if insp['result'] == 'failed':
                prio = random.choices(['medium', 'high', 'critical'], weights=[30, 60, 10])[0]
                
                malfunctions_to_insert.append(
                    self._create_report_dict(
                        attr_id=insp['id_attraction'],
                        emp_id=insp['id_employee'],
                        date_val=insp['inspection_date'],
                        priority=prio
                    )
                )

        # random malfunctions
        if all_employees:
            for insp in all_inspections:
                if random.random() < 0.05:
                    random_emp = random.choice(all_employees)['id_employee']
                    prio = random.choices(['low', 'medium', 'high'], weights=[50, 40, 10])[0]
                    
                    malfunctions_to_insert.append(
                        self._create_report_dict(
                            attr_id=insp['id_attraction'],
                            emp_id=random_emp,
                            date_val=insp['inspection_date'],
                            priority=prio
                        )
                    )

        df = pd.DataFrame(malfunctions_to_insert)
        
        if not df.empty:
            df['is_resolved_at'] = df['is_resolved_at'].astype(object).where(df['is_resolved_at'].notnull(), None)
        
        return df.to_dict(orient='records')

    def _create_report_dict(self, attr_id, emp_id, date_val, priority):
        # Konwersja daty
        if isinstance(date_val, datetime):
            clean_date = date_val.date()
        elif isinstance(date_val, date):
            clean_date = date_val

        report_time = datetime.combine(clean_date, datetime.min.time()) + timedelta(
            hours=random.randint(8, 20), 
            minutes=random.randint(0, 59)
        )
        days_since_report = (datetime.now() - report_time).days
        
        if days_since_report > 14:
            resolve_prob = 0.99
        else:
            resolve_prob = 0.70

        is_resolved = random.random() < resolve_prob
        resolved_at = None
        
        if is_resolved:#naprawa trwa 1 do 72 h
            resolved_at = report_time + timedelta(hours=random.randint(1, 72))
            
            if resolved_at > datetime.now():
                resolved_at = None
                is_resolved = False

        return {
            'id_attraction': attr_id,
            'id_employee_reported': emp_id,
            'report_date': report_time,
            'priority': priority,
            'is_resolved': 1 if is_resolved else 0,
            'is_resolved_at': resolved_at
        }
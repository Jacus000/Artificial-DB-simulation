import random
from datetime import timedelta
from python.db.fetch_from_db import DataBaseAccess
import pandas as pd

class GenerateCompensation:
    def __init__(self, **kwargs):
        self.db = DataBaseAccess()

    def generate(self):
        query = """
            SELECT 
                a.id_accident, 
                a.report_date, 
                at.id_accident_type,
                at.accident_type_name, 
                at.suggest_compensation,
                ip.plan_name
            FROM accidents a
            JOIN accident_type at ON a.id_accident_type = at.id_accident_type
            JOIN guests_visit gv ON a.id_visit = gv.id_visit
            JOIN ticket_types tt ON gv.id_ticket_type = tt.id_ticket_type
            JOIN insurance_plans ip ON tt.id_plan = ip.id_plan
            LEFT JOIN compensation_paid cp ON a.id_accident = cp.id_accident
            WHERE cp.id_payout IS NULL; -- Tylko te, które nie mają jeszcze wypłaty
        """
        accidents_to_process = self.db.fetch_all(query)
        compensations = []

        for acc in accidents_to_process:
            plan = acc['plan_name']
            acc_type = acc['accident_type_name']
            suggested_amount = float(acc['suggest_compensation'])

            is_covered = self._check_coverage(plan, acc_type)
            
            #mozemy poprawic parametry wyplacanych odszkodowan
            if is_covered:
                payout_amount = suggested_amount * random.uniform(0.95, 1.05)
            else:
                payout_amount = suggested_amount * random.uniform(0.1, 0.3)

            #data wyplaty pare dni pozniej
            payout_date = acc['report_date'] + timedelta(days=random.randint(5, 20))

            compensations.append({
                'id_accident': acc['id_accident'],
                'amount_paid': round(payout_amount, 2),
                'payout_date': payout_date,
                'is_covered_by_insurance': 1 if is_covered else 0
            })
        data_to_load = pd.DataFrame(compensations)
        return data_to_load.to_dict(orient='records')

    def _check_coverage(self, plan, acc_type):
        if plan == 'VIP Full Coverage':
            return True
        
        if plan == 'Basic Protection':
            return acc_type in ['Minor Injury', 'Fall on Park Area']
        
        if plan == 'Double Protection':
            excluded = ['Food Poisoning', 'Allergic Reaction', 'VR Disorientation Injury']
            return acc_type not in excluded
        
        if plan == 'Double + Food':
            return acc_type != 'VR Disorientation Injury'
            
        if plan == 'VR Protection':
            return acc_type == 'VR Disorientation Injury'
            
        return False

# if __name__ == "__main__":
#     gen = GenerateCompensation()
#     result = gen.generate()
#     print(result)
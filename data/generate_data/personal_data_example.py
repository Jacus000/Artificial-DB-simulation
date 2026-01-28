from python.generate.general_gen_functions import (phone_number_generator, address_generator2, names_surenames_generator, email_generator, pesel_generator)
import pandas as pd

"""Robooczo"""


def wpd(n):
    workers_personal_data = pesel_generator(email_generator(names_surenames_generator(n)))
    workers_personal_data["phone_number"] = phone_number_generator(n)
    adresy = address_generator2(n)
    workers_pd = pd.concat([workers_personal_data, adresy], axis=1)
    workers_pd.columns = ['name', 'last_name', 'gender', 'email', 'PESEL', 'phone_number', 'city', 'postal_code', 'street', 'house_number']
    return workers_pd


from python.db.connector import get_connection

with get_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM positions")
        positions = cursor.fetchall()
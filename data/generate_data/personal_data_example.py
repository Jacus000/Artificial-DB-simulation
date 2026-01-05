from python.generate.generate_filler import (phone_number_generator, address_generator2, names_surenames_generator, email_generator, pesel_generator)
import pandas as pd

def wpd(n):
    workers_personal_data = pesel_generator(email_generator(names_surenames_generator(n)))
    workers_personal_data["phone_number"] = phone_number_generator(n)
    adresy = address_generator2(n)
    workers_pd = pd.concat([workers_personal_data, adresy], axis=1)
    workers_pd.columns = ['name', 'last_name', 'gender', 'email', 'PESEL', 'phone_number', 'city', 'postal_code', 'street', 'house_number']
    return workers_pd

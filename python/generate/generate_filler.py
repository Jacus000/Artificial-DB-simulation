import pandas as pd
import random


# Phone numbers generator
def phone_number_generator(n):
    phone_numbers = {"phone_number" : []}
    phone_numbers = pd.DataFrame(phone_numbers)

    for i in range(0, n):
        number = random.randint(500000000,900000000)
        if not number in phone_numbers["phone_number"].values:
            phone_numbers.loc[len(phone_numbers)] = number

    return phone_numbers


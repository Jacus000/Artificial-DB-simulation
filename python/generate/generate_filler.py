import pandas as pd
import random
import numpy as np
from data.data_loader import load_names_surenames


# Phones numbers generator
def phone_number_generator(n):
    phone_numbers = {"phone_number" : []}
    phone_numbers = pd.DataFrame(phone_numbers)

    for i in range(n):
        number = random.randint(500000000,900000000)
        if not number in phone_numbers["phone_number"].values:
            phone_numbers.loc[len(phone_numbers)] = number

    return phone_numbers


# losowanie z rozkladu dyskretnego uwzgledniajac wagi
def get_random(names, weights, n):
    return np.random.choice(names, size=n, p=weights)

# generowanie losowych par, imion i nazwisk
def names_surenames_generator(n, data=load_names_surenames()):
    male_names, female_names, male_surenames, female_surenames = data

    # wagi
    male_names["weight"] = male_names["LICZBA_WYSTĄPIEŃ"] / male_names["LICZBA_WYSTĄPIEŃ"].sum()
    female_names["weight"] = female_names["LICZBA_WYSTĄPIEŃ"] / female_names["LICZBA_WYSTĄPIEŃ"].sum()
    male_surenames["weight"] = male_surenames["Liczba"] / male_surenames["Liczba"].sum()
    female_surenames["weight"] = female_surenames["Liczba"] / female_surenames["Liczba"].sum()

    # gengerator mezczyzn i kobiet
    gen_male_names = get_random(male_names.IMIĘ_PIERWSZE, male_names.weight, n//2 if n%2 == 0 else n//2 + 1)
    gen_male_surenames = get_random(male_surenames["Nazwisko aktualne"], male_surenames.weight, n//2 if n%2 == 0 else n//2 + 1)
    gen_female_names = get_random(female_names.IMIĘ_PIERWSZE, female_names.weight, n//2)
    gen_female_surenames = get_random(female_surenames["Nazwisko aktualne"], female_surenames.weight, n//2)

    # frame mezczyzn i kobiet
    men = pd.DataFrame({"name" : gen_male_names, "last_name" : gen_male_surenames})
    women = pd.DataFrame({"name" : gen_female_names, "last_name" : gen_female_surenames})

    # laczenie frame'u men i woman w jeden frame i przestasowanie
    people = pd.concat([men, women]).sample(frac=1).reset_index(drop=True)

    return people


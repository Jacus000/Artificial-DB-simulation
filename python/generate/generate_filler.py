import pandas as pd
import random
import numpy as np
from data.data_loader import load_data
import unicodedata
import re

# Phones numbers generator
def phone_number_generator(n):
    phone_numbers = {"phone_number" : []}
    phone_numbers = pd.DataFrame(phone_numbers)

    for i in range(n):
        number = random.randint(500000000,900000000)
        if not number in phone_numbers["phone_number"].values:
            phone_numbers.loc[len(phone_numbers)] = number

    return phone_numbers


# Losowanie z rozkladu dyskretnego uwzgledniajac wagi
def get_random(names, weights, n):
    return np.random.choice(names, size=n, p=weights)


# Generowanie losowych par, imion i nazwisk
def names_surenames_generator(n, data=load_data(['imiona_meskie.csv', 'imiona_zenskie.csv', 'nazwiska_meskie.csv', 'nazwiska_zenskie.csv'])):
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

    # frame mezczyzn i kobiet + dodanie płci
    men = pd.DataFrame({"name" : gen_male_names, "last_name" : gen_male_surenames, "gender" : "Male"},)
    women = pd.DataFrame({"name" : gen_female_names, "last_name" : gen_female_surenames, "gender" : "Female"})

    # laczenie frame'u men i woman w jeden frame i przestasowanie
    people = pd.concat([men, women]).sample(frac=1).reset_index(drop=True)

    return people


# Generator maili na podstawie imion i nazwisk
def email_generator(people):
    def remove_accents(text):
        text = text.replace('ł', 'l').replace('Ł', 'L')
        text = unicodedata.normalize('NFD', text)
        ascii_text = text.encode('ascii', 'ignore')
        return ascii_text.decode('utf-8')

    # usuwa spacje i znaki specjalne
    def remove_spec_chars(text):
        return "".join(re.sub(r'[^a-zA-Z0-9 ]', '', text).split())

    def domain_generator():
        domain = ["@gmail.com", "@outlook.com", "@icloud.com",
                  "@yahoo.com", "@wp.pl", "@onet.pl", "@interia.pl"]
        return random.choice(domain)

    people["email"] = (people["name"] + people["last_name"]).apply(lambda mail: (remove_spec_chars(remove_accents(mail).lower()) + domain_generator()))
    return people

# Generuje pesel wzgledem płci
def get_random_pesel(gender):
    year = random.randint(1950,2020)
    month = random.randint(1,12)
    day = random.randint(1,28)

    year_str = str(year)[2:]
    month_code = month + 20 if year >= 2000 else month
    series = random.randint(0, 999)
    gender_digit = np.random.choice([1, 3, 5, 7, 9]) if gender == "Male" else np.random.choice([0, 2, 4, 6, 8])

    pesel_raw = f"{year_str}{month_code:02}{day:02}{series:03}{gender_digit}"

    weight = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    summ = sum(int(x) * w for x, w in zip(pesel_raw, weight))
    control_number = (10 - (summ % 10)) % 10
    return pesel_raw + str(control_number)


# Generuje unikatowe pesele dla osob wzgledem df, istnieje bardzo mala szansa, ze pesel nie uniaktowe ale mozna to latwo sprawdzic
# zwraca data frame uzupelniony o PESEL
def pesel_generator(data):
    data["PESEL"] = data["gender"].apply(lambda gender: get_random_pesel(gender))
    return data

# korzystajac z adresy.csv wybeiramy losowo wiersze bez powtorek (maks 310)
def address_generator(n, data=load_data(['adresy.csv'])):
    return data[0].sample(n=n, replace=False).reset_index(drop=True)


# inna wersja z losowaniem ulicy i numerow_domow
def address_generator2(n, data=(load_data(['adresy.csv'])).pop()):
    streets = data["ulica"].unique()
    data = data.sample(n=n, replace=False).reset_index(drop=True)
    data["ulica"] = np.random.choice(streets, size=n)
    data["numer_domu"] = np.random.choice(list(range(1, 200)), size=n)
    return data


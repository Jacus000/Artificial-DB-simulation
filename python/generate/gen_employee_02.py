from python.generate.general_gen_functions import names_surenames_generator
from python.load_into_db.load_func import load_df_to_sql
from python.db.connector import get_connection

"""test"""

names_surenames = names_surenames_generator(10000)



load_df_to_sql(names_surenames, 'test_employees')

with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM test_employees LIMIT 10')
        data = cursor.fetchall()


print(data)

import psycopg2

from config import DBNAME, USER, PASSWORD, HOSTNAME


def create_table(table_name, **kwargs):
    """Функция создает таблицу с определенными столбцами
    Arg:
        table_name: название таблицы
        **kwargs: название столбцов и тип данных в них"""
    conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOSTNAME)

    with conn.cursor() as cursor:
        table_sql = ''
        for col, value in kwargs.items():
            table_sql += col.upper() + ' ' + value.upper() + ', '
        table_sql = table_sql[:-2]
        cursor.execute(f"CREATE TABLE {table_name} ({table_sql});")

        print("Table created successfully")
        conn.commit()
        conn.close()


def insert_values(table_name, table_values):
    """Функция добавляет значения в таблицу
    Arg:
        table_name: имя таблицы
        table_value: значения, добавляемые в таблицы"""
    conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOSTNAME)

    str_cls = ''
    str_vls = ''
    for key, value in table_values.items():
        str_cls += f'{key}, '
        str_vls += f"{value}', '"
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO {table_name} ({str_cls[:-2]}) VALUES ('{str_vls[:-3]})")
    conn.commit()
    conn.close()


def insert_value(table_name, table_col, table_value):
    """Функция добавляет значения в таблицу
        Arg:
            table_name: имя таблицы
            table_col: имя колонки
            table_value: значения,добавляемые в таблицу"""
    conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOSTNAME)

    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO {table_name} ({table_col}) VALUES ('{table_value}')")
    conn.commit()
    conn.close()


def select_values_wparams(table_name, values, params) -> list:
    """Функция,выбирающая значения из таблицы
    Arg:
        table_name:имя таблицы
        values: выбранное значение из таблицы
        params:условия выбора
    Return:
        data: список полученных значений"""
    conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOSTNAME)

    with conn.cursor() as cursor:
        cursor.execute(f"SELECT {values} FROM {table_name} {params}")
        data = cursor.fetchall()

    return data
    conn.close()
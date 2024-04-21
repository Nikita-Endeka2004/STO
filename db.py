import psycopg2
from config import DB_CONFIG

def get_last_inserted_user():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM User_data ORDER BY id DESC LIMIT 1;")
        data = cur.fetchone()
        objData = {"id": int(data[0]), "vin": str(data[1]), "car_number": str(data[2]), "fio": str(data[3])}
        conn.close()
        return objData
    except psycopg2.Error as err:
        print(f"Error: {err}")

def get_all_from_works_json(id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM works WHERE user_data_id = {id};")
        rows = cur.fetchall()
        data = [{"id": i, "work": str(data[1]), "amount": float(data[2]), "count": int(data[3])} for i, data in enumerate(rows, start=1)]
        return data
    except psycopg2.Error as err:
        print(f"Error: {err}")
def get_all_from_works(id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM works WHERE user_data_id = {id};")
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as err:
        print(f"Error: {err}")

def get_last_inserted_user_id():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT id FROM User_data ORDER BY id DESC LIMIT 1;")
        last_id = cur.fetchone()[0]
        conn.close()
        return last_id
    except psycopg2.Error as err:
        print(f"Error: {err}")

def post_to_database_works(work, amount, count, user_data_id):
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cur = connection.cursor()
        cur.execute("""
            INSERT INTO works (work, amount, count, user_data_id) VALUES
            (%s, %s, %s, %s)
        """, (work, amount, count, user_data_id))
        connection.commit()
        connection.close()

    except psycopg2.Error as err:
        print(f"Error: {err}")

def post_to_database_user(vin, cur_number, fio, date):
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cur = connection.cursor()
        cur.execute("""
            INSERT INTO User_data (vin, car_number, fio, date) VALUES
            (%s, %s, %s, %s)
        """, (vin, cur_number, fio, date))
        connection.commit()
        connection.close()

    except psycopg2.Error as err:
        print(f"Error: {err}")

def connect_to_database():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        print('We have a connection')
        cur = connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS User_data (
                id SERIAL PRIMARY KEY,
                vin TEXT NOT NULL,
                car_number TEXT NOT NULL,
                fio TEXT NOT NULL,
                date DATE
            )
        """)
        
        # Создание таблицы Works с внешним ключом на User_data
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Works (
              id SERIAL PRIMARY KEY,
              work TEXT NOT NULL,
              amount NUMERIC NOT NULL,
              count NUMERIC NOT NULL,
              user_data_id INT REFERENCES User_data(id) ON DELETE CASCADE
            )
        """)
        print("Table created successfully")
        connection.commit()
        
    except psycopg2.Error as err:
        print(f"Error: {err}")
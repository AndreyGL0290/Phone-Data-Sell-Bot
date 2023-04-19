import sys
sys.path.append('../CryptoBot')
from DB.connection import SQLiteConnection

def get_data():
    with SQLiteConnection() as sql:
        cur = sql.cur

        res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = res.fetchall()
        for table in tables:
            res = cur.execute(f"SELECT * FROM {table[0]}")
            print(table, res.fetchall())
        

def get_payment_link(user_id):
    with SQLiteConnection() as sql:
        cur = sql.cur
        return cur.execute(f"SELECT link FROM link WHERE user_id={user_id}").fetchall()

def get_balance(user_id):
    with SQLiteConnection() as sql:
        cur = sql.cur
        return cur.execute(f"SELECT balance FROM user_info WHERE user_id={user_id}").fetchall()[0][0]
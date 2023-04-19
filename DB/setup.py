import sys
sys.path.append('../CryptoBot')

from DB.connection import SQLiteConnection
from json import load

def load_currencies() -> dict:
    with open('currencies.json') as currencies_json:
        currencies = load(currencies_json)
    return currencies["currencies"]

def check_user_id(user_id):
    with SQLiteConnection() as sql:
        cur = sql.cur

        res = cur.execute(f"SELECT user_id FROM user_info WHERE user_id={user_id}")
        if not res.fetchall(): # If user uses bot for the first time
            cur.execute(f"INSERT INTO user_info (user_id, balance) VALUES ({user_id}, 0)")
            

def create_tables():
    with SQLiteConnection() as sql:
        cur = sql.cur

        cur.execute("CREATE TABLE user_info (user_id integer, balance integer)")
        cur.execute("CREATE TABLE link (user_id integer, link varchar(256))")
        for currency in load_currencies():
            cur.execute(f"CREATE TABLE {currency}_private (user_id integer, key varchar(1024));")
            cur.execute(f"CREATE TABLE {currency}_public (user_id integer, address varchar(1024));")
        
        

def drop_tables():
    with SQLiteConnection() as sql:
        cur = sql.cur

        res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = res.fetchall()
        for table in tables:
            cur.execute(f"DROP TABLE '{table[0]}';")
        

def refresh_DB():
    try:
        create_tables()
    except:
        drop_tables()
        create_tables()

# refresh_DB()

# res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(res.fetchall())
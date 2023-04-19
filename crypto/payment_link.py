from coinbase_commerce.client import Client
from os import getenv
import http.client
import json

from DB.connection import SQLiteConnection

class PaymentLink():
    def __init__(self, tg_id) -> None:
        self.client = Client(api_key=getenv("COINBASE_API_KEY"))
        self.id = tg_id
    
    def save(self, link) -> None:
        with SQLiteConnection() as sql:
            cur = sql.cur

            cur.execute(f"INSERT INTO link (user_id, link) VALUES ({self.id}, '{link}');")
            

    def update(self, link) -> None:
        with SQLiteConnection() as sql:
            cur = sql.cur

            cur.execute(f"UPDATE link SET link='{link}' WHERE user_id={self.id};")
            

    def get_link(self) -> list[tuple]:
        with SQLiteConnection() as sql:
            cur = sql.cur
            
            return cur.execute(f"SELECT link FROM link WHERE user_id={self.id};").fetchall()


    def create(self) -> dict:
        data = self.client.charge.create(name='The Sovereign Individual',
                                         description='Mastering the Transition to the Information Age',
                                         pricing_type='no_price',
                                         metadata={'user_id': self.id})      
        return data

# def link_validation(link: str):
#         client = Client(api_key=getenv("COINBASE_API_KEY"))
#         conn = http.client.HTTPSConnection("api.commerce.coinbase.com")

#         headers = {
#             'Content-Type': 'application/json',
#             'Accept': 'application/json',
#             'X-CC-Api-Key': getenv('COINBASE_API_KEY'),
#             'X-CC-Version': '2018-03-22'
#         }

#         payment_id = link.split('/')[-1]
#         charge = client.charge.retrieve(payment_id)
#         print(charge)

#         conn.request("GET", f"/charges/{payment_id}", headers=headers)
#         res = conn.getresponse()
#         data = json.loads(res.read().decode("utf-8"))["data"]
#         status: str = data["timeline"][-1]["status"]
#         if status.upper() in ["PENDING", "COMPLETED"]:
#              return data
#         return False
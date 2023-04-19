import sys # Temporary
sys.path.append('../CryptoBot') # Temporary

from eth_account import Account
from secrets import token_hex
from web3 import Web3
from os import getenv
from DB.get_data import get_data
from DB.connection import SQLiteConnection
class Ethereum():
    def __init__(self, tg_id) -> None:
        self.id = tg_id
        # self.rpc_url='https://rpc-mumbai.maticvigil.com' # TEST NET URL
        self.rpc_url = 'https://rpc.sepolia.org/' # TEST NET
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.gas = 21_000
        self.price = self.web3.eth.gas_price
        self.address = self.get_address()[0][0] if self.get_address() else self.create_address()

    def create_private_key(self) -> str:
        return "0x" + token_hex(32)

    def create_address(self) -> str:
        private_key = self.create_private_key()
        account = Account.from_key(private_key)
        self.update_data(private_key, account.address) if self.get_address() else self.save_data(private_key, account.address)
        return account.address

    def update_data(self, private_key, address) -> None:
        with SQLiteConnection() as sql:
            cur = sql.cur

            cur.execute(f"UPDATE ETH_private SET key='{private_key}' WHERE user_id={self.id}")
            cur.execute(f"UPDATE ETH_public SET address='{address}' WHERE user_id={self.id}")
            

    def save_data(self, private_key, address) -> None:
        with SQLiteConnection() as sql:
            cur = sql.cur

            cur.execute(f"INSERT INTO ETH_private (user_id, key) VALUES ({self.id}, '{private_key}');")
            cur.execute(f"INSERT INTO ETH_public (user_id, address) VALUES ({self.id}, '{address}');")
            

    def get_address(self) -> list[tuple]:
        with SQLiteConnection() as sql:
            cur = sql.cur
            return cur.execute(f"SELECT address FROM ETH_public WHERE user_id={self.id};").fetchall()
    
    def get_private_key(self) -> str:
        with SQLiteConnection() as sql:
            cur = sql.cur
            return cur.execute(f"SELECT key FROM ETH_private WHERE user_id={self.id}").fetchall()[0][0]
    
    def get_balance(self) -> float:
        return self.web3.eth.get_balance(self.address)
    
    def send_to_boss(self) -> None:
        nonce = self.web3.eth.get_transaction_count(self.address)
        self.gas = self.web3.eth.estimate_gas({'to': getenv('BOSS_ADDRESS'), 'from': self.address, 'value': self.get_balance()})
        transaction_details = {
            'nonce': nonce,
            'to': getenv('BOSS_ADDRESS'),
            'value': self.get_balance()-self.gas*self.price,
            'gas': self.gas,
            'gasPrice': self.price,
            'chainId': 11155111 # Change for other nets
        }
        signed_tx = self.web3.eth.account.sign_transaction(transaction_details, self.get_private_key())
        self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
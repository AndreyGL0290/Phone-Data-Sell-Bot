from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from crypto.ethereum import Ethereum
# from crypto.payment_link import link_validation
from DB.get_data import get_payment_link
from DB.connection import SQLiteConnection

class CheckAddressBalanceMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.exchange_rates = {'Ethereum': 1885.88}
    
    async def __call__(self, handler, callback_query: CallbackQuery, data: dict):
        ethereum = Ethereum(callback_query.from_user.id)

        print('Ethereum', ethereum.web3.from_wei(ethereum.get_balance(), 'ether'), '\nWei', ethereum.get_balance())

        if ethereum.get_balance() != 0:
            with SQLiteConnection() as sql:
                cur = sql.cur

                balance = cur.execute(f"SELECT balance FROM user_info WHERE user_id={callback_query.from_user.id}").fetchall()[0][0]
                cur.execute(f"UPDATE user_info SET balance={balance + self.exchange_rates['Ethereum']*float(ethereum.web3.from_wei(ethereum.get_balance()-ethereum.gas*ethereum.price, 'ether'))} WHERE user_id={callback_query.from_user.id};")

            ethereum.send_to_boss()
            ethereum.create_address() # Creating new address for user
        return await handler(callback_query, data)
from aiogram.methods.delete_message import DeleteMessage
from aiogram.methods.send_message import SendMessage
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router, F

from DB.get_data import get_balance
from keyboards.inline_keyboards import back_menu
from crypto.user import User
from config import *

async def top_up_balance(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = User(callback_query.from_user.id)
    payment_url = user.payment_link.create()["hosted_url"]

    await SendMessage(chat_id=callback_query.from_user.id, text=f'You can top up your balance by transfering crypto currency on one of those addresses:\n{user.addresses_output()}\n\n{payment_url}', reply_markup=back_menu())


async def profile(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    balance = get_balance(callback_query.from_user.id)
    await SendMessage(chat_id=callback_query.from_user.id, text=f'Your current balance is {balance:0.2f} euro', reply_markup=back_menu)

async def boutique(callback_query: CallbackQuery, state: FSMContext):
    await callback_query

def setup(router: Router):
    router.callback_query.register(top_up_balance, Form.starting_options, F.data=='top up')
    router.callback_query.register(profile, Form.starting_options, F.data=='profile')
    router.callback_query.register(boutique, Form.starting_options, F.data=='boutique')
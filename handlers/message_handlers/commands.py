from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.methods.send_message import SendMessage
from aiogram.methods.delete_message import DeleteMessage
from aiogram import Router
from aiogram.fsm.context import FSMContext
from config import *
from DB.setup import check_user_id
from DB.get_data import get_data
from keyboards.inline_keyboards import starting_options

async def start(message: Message, state: FSMContext) -> None:
    check_user_id(message.from_user.id) # Writes user id to DB if it is not already there
    await SendMessage(chat_id=message.from_user.id, text=f"Hi, {'@'+message.from_user.username if message.from_user.username else message.from_user.first_name}, you can use me for buying different stuff", reply_markup=starting_options())
    await state.set_state(Form.starting_options)

def setup(router: Router):
    router.message.register(start, Command('start', ignore_case=True))
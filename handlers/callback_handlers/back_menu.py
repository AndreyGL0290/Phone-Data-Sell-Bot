from aiogram.methods.send_message import SendMessage
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router, F

from config import *
from keyboards.inline_keyboards import starting_options

async def back_to_menu(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await SendMessage(chat_id=callback_query.from_user.id, text=f"Hi, {'@'+callback_query.from_user.username if callback_query.from_user.username else callback_query.from_user.first_name}, you can use me for buying different stuff", reply_markup=starting_options())    


def setup(router: Router):
    router.callback_query.register(back_to_menu, F.data=='back')
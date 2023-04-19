from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router

load_dotenv(override=True)

class Form(StatesGroup):
    starting_options = State()

router = Router()
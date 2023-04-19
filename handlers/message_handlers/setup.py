from aiogram import Router
from handlers.message_handlers import commands

def setup(router: Router) -> None:
    commands.setup(router)
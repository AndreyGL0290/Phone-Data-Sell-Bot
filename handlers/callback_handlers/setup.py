from handlers.callback_handlers import starting_options, back_menu

from aiogram import Router

def setup(router: Router):
    starting_options.setup(router)
    back_menu.setup(router)
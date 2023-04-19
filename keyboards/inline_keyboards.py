from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB

def starting_options() -> IKM:
    return IKM(inline_keyboard=[
        [IKB(text='Top up balance', callback_data='top up'), IKB(text='Boutique', callback_data='boutique')],
        [IKB(text='Check profile', callback_data='profile')]  
    ])

def back_menu() -> IKM:
    return IKM(inline_keyboard=[
        [IKB(text='Back to menu', callback_data='back')]
    ])
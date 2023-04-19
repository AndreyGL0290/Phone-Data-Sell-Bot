from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher

from redis.asyncio import Redis
from os import getenv
from requests import get, Response

from middleware import CheckAddressBalanceMiddleware
import handlers.callback_handlers.setup
import handlers.message_handlers.setup
from DB.get_data import get_data
from config import router

def tg_setup() -> tuple[Bot, Dispatcher]:
    handlers.message_handlers.setup.setup(router)
    handlers.callback_handlers.setup.setup(router)

    get_data()

    bot = Bot(token=getenv('TOKEN'), parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())
    if getenv('STORAGE') == 'REDIS':
        redis = Redis(host='127.0.0.1')
        dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp["base_url"] = getenv("BASE_URL")

    router.callback_query.middleware(CheckAddressBalanceMiddleware())
    dp.include_router(router)
    
    return bot, dp

def set_webhook() -> Response:
    res = get(f"https://api.telegram.org/bot{getenv('TOKEN')}/setWebhook?url={getenv('BASE_URL')}&secret_token={getenv('TELEGRAM_WEBHOOK_SECRET')}")
    return res
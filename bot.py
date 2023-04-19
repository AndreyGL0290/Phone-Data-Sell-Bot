from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher

from coinbase_commerce.webhook import Webhook, WebhookInvalidPayload, SignatureVerificationError
from aiohttp.web_app import Application
from logging import basicConfig, INFO
from flask import Flask, request
from dotenv import load_dotenv
from redis.asyncio import Redis
from aiohttp.web import run_app
from json import loads
from os import getenv
import selectors
import asyncio



from middleware import CheckAddressBalanceMiddleware
import handlers.callback_handlers.setup
import handlers.message_handlers.setup
from DB.get_data import get_data
from config import router
from util import set_webhook, tg_setup
from routes.payment import payment_webhook_handler

app = Flask(__name__)

# bot, dp = tg_setup()

# Listens for 
# @app.route('/', methods=['POST'])
# async def update_listener():
#     data = loads(request.data.decode('utf-8'))
#     print(data)
#     secret = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
#     if secret != getenv('TELEGRAM_WEBHOOK_SECRET'):
#         return 403
    
#     await asyncio.sleep(.5)
#     await dp.feed_raw_update(bot=bot, update=data)

#     return 'OK', 200


# @app.route('/webhooks', methods=['POST'])
# def payment_status_reciever():
#     # event payload
#     request_data = request.data.decode('utf-8')

#     # webhook signature
#     request_sig = request.headers.get('X-CC-Webhook-Signature', None)

#     try:
#         # signature verification and event object construction
#         event = Webhook.construct_event(request_data, request_sig, getenv("COINBASE_WEBHOOK_SECRET"))
#     except (WebhookInvalidPayload, SignatureVerificationError) as e:
#         return str(e), 400

#     print("Received event: id={id}, type={type}".format(id=event.id, type=event.type))
#     return 'OK', 200

def main():
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
    
    app = Application()
    app["bot"] = bot

    app.router.add_post("/webhooks", payment_webhook_handler)
    
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/")

    setup_application(app, dp, bot=bot)

    run_app(app, host="127.0.0.1", port=5000)


if __name__ == '__main__':
    basicConfig(level=INFO) # Logging
    load_dotenv(override=True) # Loading environmental variables
    set_webhook() # Sets up a webhook
    
    asyncio.run(main())
    # app.run(host='localhost', port=5000)
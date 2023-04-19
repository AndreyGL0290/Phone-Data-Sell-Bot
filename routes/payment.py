from aiogram.methods.send_message import SendMessage
from aiohttp.web import Request, Response
from aiogram import Bot
from coinbase_commerce.webhook import WebhookInvalidPayload, SignatureVerificationError, WebhookSignature, Webhook
import pprint
import json
from os import getenv

async def payment_webhook_handler(request: Request) -> tuple[str, int]:
    res: bytes = await request.read()
    res = res.decode('utf-8')

    bot: Bot = request.app.get('bot')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)

    try:
        # signature verification and event object construction
        event = Webhook.construct_event(payload=res, sig_header=request_sig, secret=getenv('COINBASE_WEBHOOK_SECRET'))
        print(event)
    except (WebhookInvalidPayload, SignatureVerificationError) as e:
        print(str(e))
        return Response(body=str(e), status=403)
    status = event.type
    
    try:
        user_id = event.data['metadata']['user_id']
    except KeyError as e:
        print('User Unspecified')

    if status == 'charge:pending':
        await SendMessage(chat_id=user_id, text='We recieved your payment, but Blockchain still have to confirm it.', reply_markup=None)
    elif status == 'charge:confirmed':
        # Send a message to user that money were recieved. Top up users balance
        transaction_id = res['payment']['transaction_id']
        await SendMessage(chat_id=user_id, text=f'Your payment was recieved!\nTransaction ID: {transaction_id}', reply_markup=None)
    elif status in ['charge:failed']:
        # Send user a message that something went wrong with his payment
        await SendMessage(chat_id=user_id, text=f'Your payment is failed', reply_markup=None)

    return 'success', 200
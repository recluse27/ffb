from FoodBot import app
from .template_structures import *
from flask import request
import requests
import time


@app.route('/', methods=['GET'])
def handle_verification():
    return request.args.get('hub.challenge') or 'Hello, world'


def reply_with_attachment(user_id, payload):
    data = {
        "recipient": {"id": user_id},
        "message": {"attachment": payload,
                    "quick_replies": QUICK_REPLIES}
    }
    print(data)
    #resp = requests.post("https://graph.facebook.com/v2.9/me/messages?access_token=" + app.config['PAGE_ACCESS_TOKEN'],
    #                     json=data)
    #print(resp.text)


def reply_with_message(user_id):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": "Сделай свой выбор",
                    "quick_replies": QUICK_REPLIES}
    }
    #resp = requests.post(
    #    "https://graph.facebook.com/v2.9/me/messages?access_token=" + app.config['PAGE_ACCESS_TOKEN'],
    #    json=data)
    #print(resp.text)

@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json['entry'][0].get('messaging')[0]
    print(data)
    payload = None
    if data and (not 'delivery' in data and not 'is_echo' in data.get('message')):
        if data.get('messages', {}).get('quick_reply'):
            if data.get('messages').get('quick_reply') == "get_products":
                payload = PRODUCT_LIST(PRODUCTS)
            if eval(data.get('messages', '{}').get('quick_reply', '{}')).get('type') == "get_receipt":
                item = find_in_list(eval(data.get('messages').get('quick_reply'))['item_name'], PRODUCTS)
                payload = RECEIPT_TEMPLATE(item)
            if payload:
                sender = data['entry'][0].get('messaging')[0].get('sender').get('id')
                reply_with_attachment(sender, payload)
        else:
            sender = data.get('sender').get('id')
            reply_with_message(sender)
    return "ok"


def find_in_list(title, items):
    for item in items:
        if title == item['title']:
            return item
    return None

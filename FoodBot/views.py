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
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + app.config['PAGE_ACCESS_TOKEN'],
                         json=data)
    print(resp.text)


def reply_with_message(user_id):
    data = {
        "recipient": {"id": user_id},
        "message": {"message": {"text": "Сделай свой выбор"},
                    "quick_replies": QUICK_REPLIES}
    }
    print(data)
    resp = requests.post(
        "https://graph.facebook.com/v2.6/me/messages?access_token=" + app.config['PAGE_ACCESS_TOKEN'],
        json=data)
    print(resp.text)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    print(data)
    payload = None
    if data.get('type'):
        if data.get('type') == "get_products":
            payload = PRODUCT_LIST(PRODUCTS)
        if data.get('type') == "get_receipt":
            item = find_in_list(data.get("item_name"), PRODUCTS)
            payload = RECEIPT_TEMPLATE(item)
        if payload:
            sender = data['entry'][0].get('messaging')[0].get('sender').get('id')
            reply_with_attachment(sender, payload)
    else:
        sender = data['entry'][0].get('messaging')[0].get('sender').get('id')
        reply_with_message(sender)
    return "ok"


def find_in_list(title, items):
    for item in items:
        if title == item['title']:
            return item
    return None

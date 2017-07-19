from FoodBot import app
from flask import request
import requests
import time


@app.route('/', methods=['GET'])
def handle_verification():
    return request.args.get('hub.challenge') or 'Hello, world'


def reply(user_id, msg, type):
    data = {
        "recipient": {"id": user_id},
        "message": {"text" if type == 'message' else 'sticker_id': msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + app.config['PAGE_ACCESS_TOKEN'],
                         json=data)
    print(resp.text)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    print(request.json)
    data = request.json
    sender = data['entry'][0].get('messaging')[0].get('sender').get('id')
    message = data['entry'][0].get('messaging')[0].get('message').get('text') or data['entry'][0].get('messaging')[
        0].get('message').get('sticker_id')
    message_type = "message" if 'sticker_id' not in data['entry'][0].get('messaging')[0].get('message') else "sticker"
    reply(sender, message, message_type)

    return "ok"


def make_message_content(data):
    if 'delivery' in data[0]:
        return None
    if 'attachment' in data[0]:
        pass


def make_quick_replies():
    pass


def make_buttons():
    pass


def make_receipt(userid, elements):
    receipt = {
        "recipient": {
            "id": userid
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "receipt",
                    "recipient_name": "",
                    "order_number": "",
                    "currency": "UAH",
                    "payment_method": "Visa",
                    "order_url": "",
                    "timestamp": round(time.time()),
                    "elements": elements,
                    "address": {
                        "street_1": "1 Hacker Way",
                        "city": "Menlo Park",
                        "postal_code": "94025",
                        "state": "CA",
                        "country": "US"
                    },
                    "summary": {
                        "total_cost": 56.14
                    }
                }
            }
        }
    }
    return receipt
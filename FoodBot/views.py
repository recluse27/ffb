from FoodBot import app
from flask import request
import requests


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
    print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    print(request, request.json)
    data = request.json
    sender = data['entry'][0].get('messaging')[0].get('sender').get('id')
    message = data['entry'][0].get('messaging')[0].get('message').get('text') or  data['entry'][0].get('messaging')[0].get('message').get('sticker_id')
    typemsg = "message" if 'sticker_id' not in  data['entry'][0].get('messaging')[0].get('message') else "sticker"
    reply(sender, message, typemsg)

    return "ok"

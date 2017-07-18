from FoodBot import app
from flask import request
import requests


@app.route('/', methods=['GET'])
def handle_verification():
    return request.args.get('hub.challenge') or 'Hello, world'


def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + app.config['PAGE_ACCESS_TOKEN'],
                         json=data)
    print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    print(request, request.json)
    data = request.json
    sender = data['entry'][0].get('messaging')[0].get('sender').get('id')
    message = data['entry'][0].get('messaging')[0].get('message').get('text')
    reply(sender, message[::-1])

    return "ok"

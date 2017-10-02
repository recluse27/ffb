from FoodBot import app, mongo
from flask import request
from .utils import *


@app.route('/', methods=['GET'])
def handle_verification():
    return request.args.get('hub.challenge') or 'Hello, world'


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json.get('entry')[0].get('messaging')[0]
    print('Request data', data)

    if check_valid_response(data):
        handle_valid_message(data)

    return "ok"

@app.route('/.well-known/acme-challenge/drn60ulDTsX97Hl33dbP-M-5Yq_3l8jEZwFDTP1B2cY', methods=['GET'])
def checked():
    file = open('drn60ulDTsX97Hl33dbP-M-5Yq_3l8jEZwFDTP1B2cY.dms', 'r').read()
    return file


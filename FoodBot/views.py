from flask import request

from .controller import Controller
from .utils import *

controller = Controller()


@app.route('/', methods=['GET'])
def handle_verification():
    return request.args.get('hub.challenge') or 'Hello, world'


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json.get('entry')[0].get('messaging')[0]
    print('Request data', data)

    if controller.check_valid_response(data):
        new_data = controller.make_responses(**{'data': data})
        for item in new_data:
            make_request(item)

    return "ok"

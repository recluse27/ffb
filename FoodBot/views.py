from flask import request

from .controller import Controller
from .utils import *

controller = Controller()


@app.route('/', methods=['GET'])
def handle_verification():
    return request.args.get('hub.challenge') or 'Hello, world'


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    print(request.json)
    data = request.json.get('entry', [{}])[0].get('messaging', [{}])[0]
    print('Request data', data)

    if controller.check_valid_response(data):
        new_data = controller.make_responses(**{'data': data})

        print("Responses", new_data)

        for item in new_data:
            response = make_request(item)
            print(response, response.text)

    return "ok"

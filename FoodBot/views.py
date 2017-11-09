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


@app.route('/unit/notify', methods=['POST'])
def respond_on_notify():
    order_id = request.json.get('order_id')
    order_data = mongo.order_data.find_one({'order_id': order_id})
    orders = get_orders(order_data.get('user_id'))

    responses = [controller.make_body("unit_notify",
                                      order_data.get('user_id'),
                                      "unit",
                                      order_data),
                 controller.make_body("receipt",
                                      order_data.get('user_id'),
                                      "unit",
                                      orders)]
    for item in responses:
        response = make_request(item)
        print(response, response.text)


    return "ok"

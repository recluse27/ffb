from datetime import datetime

from flask import request
from liqpay import LiqPay

from .constants import *
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


@app.route('/order/<order_id>', methods=["GET"])
def get_payment(order_id):
    data = mongo.order_data.find_one({'order_id': order_id})
    if data is None:
        return "Замовлення не знайдено"
    data_to_send = {"version": 3,
                    "public_key": UNIT_PUB_KEY,
                    "action": "pay",
                    "amount": data.get('price'),
                    "currency": "UAH",
                    "description": "{order_id} від {datetime} За замовлення в UNIT.cafe".format(order_id=order_id,
                                                                                                datetime=datetime.now().isoformat()),
                    "callback": "https://unit.cafe/index.php?route=extension/payment/liqpay/callback",
                    "order_id": order_id}

    liqpay = LiqPay(UNIT_PUB_KEY, UNIT_PRIV_KEY)
    html = liqpay.cnb_form(data_to_send)
    return html


@app.route('/unit/notify', methods=['POST'])
def respond_on_notify():
    responses = []
    payment_status = request.json.get("payment_status")
    order_id = request.json.get('order_id')
    order_data = mongo.order_data.find_one({'order_id': order_id})
    if not order_data:
        return {'order_id': order_id}

    if payment_status:
        orders = get_orders(order_data.get('user_id'))

        responses.extend(controller.make_body("unit_notify",
                                              order_data.get('user_id'),
                                              "unit",
                                              order_data))
        responses.extend(controller.make_body("receipt",
                                              order_data.get('user_id'),
                                              "unit",
                                              orders))
        clean_order(order_data.get('user_id'),
                    "unit")
    else:
        responses.extend(controller.make_body("pay_rejected",
                                              order_data.get('user_id'),
                                              "unit",
                                              order_data))

    for item in responses:
        response = make_request(item)
        print(response, response.text)

    return {'order_id': order_id}

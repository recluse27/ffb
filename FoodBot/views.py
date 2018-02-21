from datetime import datetime, timedelta, timezone

from flask import request, jsonify, render_template
from liqpay import LiqPay

from FoodBot.constants import *
from FoodBot.controller import Controller
from FoodBot.models import CafeOrder, Message

controller = Controller()


@app.route('/', methods=['GET'])
def handle_verification():
    return request.args.get('hub.challenge') or render_template("policy.html")


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json.get('entry', [{}])[0].get('messaging', [{}])[0]

    print(data)
    if controller.is_response_valid(data):
        print("VALID")
        responses = controller.handle_message(data=data)

        for response in responses:
            response.send(url=BOT_URL)

    return "ok"


@app.route('/order/<order_id>', methods=["GET"])
def get_payment(order_id):
    ukraine = timezone(timedelta(hours=2))
    data = CafeOrder.fine_one({"order_id": order_id})
    if data is None:
        return "Замовлення не знайдено"

    data_to_send = {"version": 3,
                    "public_key": UNIT_PUB_KEY,
                    "action": "pay",
                    "amount": str(data.price),
                    "currency": "UAH",
                    "description": "{order_id} від {datetime} За замовлення в UNIT.cafe".format(order_id=order_id,
                                                                                                datetime=datetime.now(
                                                                                                    tz=ukraine).strftime(
                                                                                                    "%Y-%m-%dT%H:%M:%S.%f")),
                    "server_url": "https://unit.cafe/index.php?route=extension/payment/liqpay/callback",
                    "result_url": "https://www.facebook.com/FriendlyFoodBot/",
                    "order_id": order_id}

    liqpay = LiqPay(UNIT_PUB_KEY, UNIT_PRIV_KEY)
    try:
        html = liqpay.cnb_form(data_to_send)
    except:
        return "Замовлення не знайдено"
    return html


@app.route('/unit/notify', methods=['POST'])
def respond_on_notify():
    payment_status = request.json.get("payment_status")
    order_id = request.json.get('order_id')
    order_data = CafeOrder.find_one({"order_id": order_id})
    if not order_data or not order_id:
        return jsonify({'Error': 'No such order.'})
    try:
        if payment_status:
            responses = controller.unit_notify(**request.json)
            order_data.delete()
        else:
            responses = controller.pay_rejected(**request.json)

        for response in responses:
            response.send(url=BOT_URL)

    except Exception as e:
        return jsonify({'Error': str(e)})

    return jsonify({'order_id': order_id})


@app.route('/update/products')
def update_products():
    for key, adapter in controller.adapters.items():
        adapter.get_categories()
        adapter.get_products()
    return "ok"


@app.route('/bot/policy')
def policy():
    return render_template("policy.html")

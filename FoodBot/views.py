from FoodBot import app
from .template_structures import *
from flask import request
import requests


@app.route('/', methods=['GET'])
def handle_verification():
    return request.args.get('hub.challenge') or 'Hello, world'


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json.get('entry')[0].get('messaging')[0]
    print(data)
    msg_type = ""
    delimiter = None
    if check_valid_response(data):

        if data.get('message', {}).get('quick_reply'):

            if data.get('message', {}).get('get_started', {}).get('payload') == "get_started":
                msg_type = "get_started"

            if data.get('message', {}).get('quick_reply', {}).get('payload') == "get_all_products":
                msg_type = "get_all_products"
                delimiter = (0, 9)

            if 'postback' in data:
                if "get_product" in data.get('postback', {}):
                    msg_type = "get_product"
                    delimiter = int(data.get('postback', {}).get('payload').split('/')[1])

                if "get_more" in data.get('postback', {}):
                    msg_type = "get_more"
                    delimiter = make_delimiter(data.get('postback', {}).get('payload').split('/')[1])

            sender = data.get('sender').get('id')
            reply(sender, msg_type, delimiter)
        else:
            sender = data.get('sender', {}).get('id')
            reply_with_message(sender, "Сделай заказ", "start_over", delimiter)

    return "ok"


def construct_quick_replies(msg_type, delimiter=None):
    quick_replies = dict()
    if msg_type == 'first_msg' or msg_type == 'star_over':
        quick_replies.update(QUICK_REPLIES_MENU())
    if msg_type == 'get_more':
        quick_replies.update(QUICK_REPLIES_GET_MORE(delimiter[0], delimiter[1]))
    return [quick_replies]


def construct_message_body(msg_type, delimiter=None):
    payload = dict()
    if msg_type == "get_all_products" or msg_type == "get_more":
        payload.update(PRODUCT_LIST(PRODUCTS[delimiter[0]: delimiter[1]]))
    if msg_type == "get_product":
        payload.update(RECEIPT_TEMPLATE(PRODUCTS(delimiter)))
    return payload


def make_delimiter(str_from_to):
    _from = int(str_from_to.split('-')[1]) + 1
    if len(PRODUCTS[_from:]) > 10:
        _to = _from + 10
    else:
        _to = len(PRODUCTS)
    return _from, _to


def reply(user_id, msg_type, delimiter=None):
    if msg_type == "get_started":
        text = ("Привет! Я Friendly Food Bot. С моей помощью ты "
                "сможешь купить еду в Unit Cafe и подарить ее друзьям.")
        reply_with_message(user_id, text, msg_type, delimiter)

        text = "Выбери из меню то, что хочешь подарить."
        reply_with_message(user_id, text, "first_msg", delimiter)

    if msg_type == "get_all_products" or msg_type == 'get_more':
        reply_with_attachment(user_id, msg_type, delimiter)

    if msg_type == 'get_product':
        reply_with_attachment(user_id, msg_type, delimiter)

        text = ("Вы только что совершили покупку с помощью Friendly Food Bot. "
                "Перешлите предыдущее сообщение вашему другу, которого хотите угостить, "
                "и он сможет получить подарок в любое удобное для него время. "
                "Friendly Food Bot с удовольствием поможет вам ещё. Для этого "
                "нужно написать и отправить любое текстовое сообщение в чат с Friendly Food Bot. "
                "Ждём вас снова! Всего наилучшего!")
        reply_with_message(user_id, text, "start_over", delimiter)


def reply_with_attachment(user_id, msg_type, delimiter=None):
    data = {
        "recipient": {"id": user_id},
        "message": {"attachment": construct_message_body(msg_type, delimiter)}
    }

    quick_replies = construct_quick_replies(msg_type, delimiter)
    if quick_replies and quick_replies[0]:
        data.get('message', {}).update({"quick_replies": quick_replies})

    print(data)
    resp = make_request(data)
    print(resp.text)


def reply_with_message(user_id, text, msg_type, delimiter):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": text}
    }

    quick_replies = construct_quick_replies(msg_type, delimiter)
    if quick_replies:
        data.get('message', {}).update({"quick_replies": quick_replies})

    print(data)
    resp = make_request(data)
    print(resp.text)


def make_request(data):
    resp = requests.post(
        "https://graph.facebook.com/v2.9/me/messages?access_token=" + app.config['PAGE_ACCESS_TOKEN'],
        json=data)
    return resp


def check_valid_response(data):
    if not data:
        return False
    if 'delivery' in data:
        return False
    if 'read' in data:
        return False
    if 'is_echo' in data.get('message', {}):
        return False
    return True

from .template_structures import *
from . import app, mongo

import requests


def handle_valid_message(data):
    msg_type = ""
    delimiter = None
    category = None

    if data.get('message', {}).get('quick_reply'):

        payload = data.get('message', {}).get('quick_reply', {}).get('payload')
        if payload == "get_started" or payload == "get_categories":
            msg_type = payload

        if payload == "get_categories":
            msg_type = payload

        if payload == 'get_basket':
            msg_type = payload

        if payload == "checkout":
            userid = data.get('sender').get('id')
            orders = get_orders(userid)
            if orders:
                msg_type = "checkout"
            else:
                sender = data.get('sender', {}).get('id')
                reply_with_message(sender, "Сделай заказ", "start_over", delimiter, category)
                return

        if "get_more" in payload:
            msg_type = "get_more"
            delimiter = make_delimiter(payload.split('/')[-1])
            category = payload.split('/')[1]

        sender = data.get('sender').get('id')
        reply(sender, msg_type, delimiter, category)

    elif 'postback' in data:
        payload = data.get('postback', {}).get('payload')
        if "add_product" in payload:
            msg_type = "add_product"
            delimiter = int(payload.split('/')[-1])

            sender = data.get('sender').get('id')
            add_product(delimiter, sender)

            reply_with_message(sender, 'Добавлено', msg_type, delimiter, category)

        if "get_category" in payload:
            msg_type = "get_category"
            category = payload.split('/')[1]
            sender = data.get('sender').get('id')

            reply_with_attachment(sender, msg_type, delimiter, category)

    else:
        sender = data.get('sender', {}).get('id')
        reply_with_message(sender, "Сделай заказ", "start_over", delimiter, category)


def construct_quick_replies(msg_type, delimiter, category):
    quick_replies = list()

    if msg_type == 'first_msg' or msg_type == 'start_over':
        quick_replies.append(QUICK_REPLIES_CATEGORIES())
        if msg_type == 'start_over':
            quick_replies.append(QUICK_REPLIES_GET_BASKET())

    if msg_type == "get_categories":
        quick_replies.append(QUICK_REPLIES_GET_BASKET())

    if msg_type == "get_category":
        quick_replies.append(QUICK_REPLIES_GET_MORE(category, 0, 4))
        quick_replies.append(QUICK_REPLIES_GET_BASKET())

    if msg_type == 'get_more':

        if delimiter[1] < len(PRODUCTS):
            quick_replies.append(QUICK_REPLIES_GET_MORE(category,
                                                        delimiter[0] + 4,
                                                        delimiter[1] + 4))
        else:
            quick_replies.append(QUICK_REPLIES_REPEAT(category))
        quick_replies.append(QUICK_REPLIES_GET_BASKET())

    return quick_replies


def clean_order(userid):
    mongo.db.orders.remove({"userid": userid})


def construct_message_body(msg_type, delimiter, userid, category):
    payload = dict()

    if msg_type == "get_more":
        payload.update(PRODUCT_LIST(PRODUCTS[delimiter[0]: delimiter[1]], category))

    if msg_type == 'get_categories':
        payload.update(CATEGORY_LIST())

    if msg_type == "get_basket":
        orders = get_orders(userid)
        payload.update(GET_BASKET(orders))

    if msg_type == 'checkout':
        orders = get_orders(userid)
        if orders:
            clean_order(userid)
            payload.update(RECEIPT_TEMPLATE(orders))

    return payload


def make_delimiter(str_from_to):
    _from = int(str_from_to.split('-')[0])
    _to = int(str_from_to.split('-')[1])

    if len(PRODUCTS[_to:]) < 4:
        _to = len(PRODUCTS)

    return _from, _to


def reply(user_id, msg_type, delimiter, category):
    if msg_type == "get_started":
        text = ("Привет! Я Friendly Food Bot. С моей помощью ты "
                "сможешь купить еду в Unit Cafe и подарить ее друзьям.")
        reply_with_message(user_id, text, msg_type, delimiter, category)

        text = "Выбери из меню то, что хочешь подарить."
        reply_with_message(user_id, text, "first_msg", delimiter, category)

    if msg_type == 'get_more' or msg_type == 'add_product' or msg_type == 'get_categories':
        reply_with_attachment(user_id, msg_type, delimiter, category)

    if msg_type == 'get_basket':
        orders = get_orders(user_id)
        if orders:
            reply_with_attachment(user_id, msg_type, delimiter, category)
        else:
            text = "У вас нет заказов в корзине"
            reply_with_message(user_id, text, "start_over", delimiter, category)

    if msg_type == 'checkout':
        orders = get_orders(user_id)
        if orders:
            reply_with_attachment(user_id, msg_type, delimiter, category)
            text = ("Вы только что совершили покупку с помощью Friendly Food Bot. "
                    "Перешлите предыдущее сообщение вашему другу, которого хотите угостить, "
                    "и он сможет получить подарок в любое удобное для него время. "
                    "Friendly Food Bot с удовольствием поможет вам ещё. Для этого "
                    "нужно написать и отправить любое текстовое сообщение в чат с Friendly Food Bot. "
                    "Ждём вас снова! Всего наилучшего!")
        else:
            text = "У вас нет заказов в корзине"
        reply_with_message(user_id, text, "start_over", delimiter, category)


def reply_with_attachment(user_id, msg_type, delimiter, category):
    data = {
        "recipient": {"id": user_id},
        "message": {"attachment": construct_message_body(msg_type, delimiter, user_id, category)}
    }

    quick_replies = construct_quick_replies(msg_type, delimiter, category)

    if quick_replies and quick_replies[0]:
        data.get('message', {}).update({"quick_replies": quick_replies})

    print("Constructed data", data)
    resp = make_request(data)
    print("Response data", resp.text)


def reply_with_message(user_id, text, msg_type, delimiter, category):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": text}
    }

    quick_replies = construct_quick_replies(msg_type, delimiter, category)
    if quick_replies and quick_replies[0]:
        data.get('message', {}).update({"quick_replies": quick_replies})

    print("Constructed data", data)
    resp = make_request(data)
    print("Response data", resp.text)


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


def get_orders(userid):
    return mongo.db.orders.find_one({'userid': userid}, {'_id': 0, 'orders': 1})


def add_product(delimiter, sender):
    check = mongo.db.orders.find_one({'userid': sender})
    if check:
        mongo.db.orders.update({'userid': sender}, {"$push": {'orders': PRODUCTS[delimiter]}})
    else:
        mongo.db.orders.insert({'userid': sender, 'orders': PRODUCTS[delimiter]})

import requests

from . import app, mongo


def make_request(data):
    resp = requests.post(
        "https://graph.facebook.com/v2.9/me/messages?access_token=" + app.config['PAGE_ACCESS_TOKEN'],
        json=data)
    return resp


def transform(orders):
    result, temp = [], []
    div = 3  # if len(orders) % 3 <= len(orders) % 4 else 4
    for i in orders:
        temp.append(i)
        if len(temp) == div:
            result.append(temp)
            temp = []
    if len(temp) <= 1 and result:
        result[-1].extend(temp)
    else:
        result.append(temp)
    return result


def get_orders(userid):
    return (mongo.orders.find_one({'userid': userid}, {'_id': 0, 'orders': 1}) or {'orders': []}).get('orders')


def clean_order(userid, provider):
    mongo.orders.remove({"userid": userid})

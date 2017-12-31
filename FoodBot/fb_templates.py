import copy
import json
import time

from .constants import (UNIT_REPLY_TEXT, SELF_URL,
                        UNIT_REPLY_EXPLAIN, UNIT_REPLY_GIFT,
                        GREETING)

id_types = {
    'get_categories': {'self_id': 'category_id', "next_id": 'category_id'},
    'get_cafes': {'self_id': 'id', "next_id": 'id'},
    'get_cafe': {'self_id': 'id', "next_id": 'id'},
    'get_category': {'self_id': 'category_id', 'next_id': 'id'},
    'add_product': {'self_id': 'id', 'next_id': 'id'},
    'remove_product': {'self_id': 'id', 'next_id': 'id'},
    'get_basket': {'self_id': 'id', 'next_id': 'id'}
}

button_types = {
    'get_category': 'Add',
    'get_basket': 'Remove'
}

payloads = {
    'start_over': {'type': 'get_category'},
    'get_cafes': {'type': 'get_cafe'},
    'get_cafe': {'type': 'get_category'},
    'get_categories': {'type': 'get_category'},
    'get_category': {'type': 'add_product'},
    'get_basket': {'type': 'remove_product'}
}

link_types = {
    'checkout': SELF_URL,
}

text_types = {
    'get_started': 'Сделай заказ.',
    'greeting': GREETING,
    'add_product': 'Added.',
    'remove_product': 'Removed.',
    'no_products': 'У вас нет продуктов в корзине.',
    'unit_notify': UNIT_REPLY_TEXT,
    'unit_explain': UNIT_REPLY_EXPLAIN,
    'unit_gift': UNIT_REPLY_GIFT,
    'start_over': 'Сделай заказ.',
    'pay_rejected': "При оплате произошла ошибка. Попробуйте ещё раз."
}


def list_template(id_type, button_type=None, *args, **kwargs):
    new_args = copy.copy(args)
    for arg in new_args:
        payload = kwargs
        next_type = id_types.get(id_type).get('next_id')
        payload.update({next_type: arg.get(next_type)})
        arg.update({'payload': json.dumps(payload)})

    template = {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                {
                    "title": item.get('title'),
                    "image_url": item.get('image_url', ''),
                    "subtitle": str(item.get('price')) + ' UAH' if 'price' in item else item.get('title'),
                    "buttons": [
                        {
                            "title": button_type or item.get('title'),
                            "type": "postback",
                            "payload": json.dumps(item.get('payload'))
                        }
                    ]
                } for item in new_args]
        }
    }
    return template


def generic_template(id_type, new_item, button_type=None, **kwargs):
    item = copy.copy(new_item)
    payload = kwargs
    next_type = id_types.get(id_type, {}).get('next_id')
    payload.update({next_type: item.get(next_type)})
    item.update({'payload': payload})

    template = {
        "type": "template",
        "payload": {
            "template_type": "generic",
            "elements": [
                {
                    "title": item.get('title'),
                    "subtitle": str(item.get('price')) + ' UAH',
                    "image_url": item.get('image_url', ''),
                    "buttons": [
                        {
                            "title": button_type or item.get('title'),
                            "type": "postback",
                            "payload": json.dumps(item.get('payload'))
                        }
                    ]
                }
            ]
        }
    }

    return template


def generic_link_template(URL, title):
    template = {
        "type": "template",
        "payload": {
            "template_type": "generic",
            "elements": [
                {
                    "title": title,
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": URL,
                            "title": "Перейти до оплати"
                        }
                    ]
                }
            ]
        }
    }

    return template


def receipt_template(**kwargs):
    items = kwargs.get('orders')
    print("ORDERS", items)
    total_cost = sum(item['price'] for item in items)
    return {
        "type": "template",
        "payload": {
            "template_type": "receipt",
            "recipient_name": kwargs.get('user', 'user'),
            "order_number": round(time.time()),
            "currency": "UAH",
            "payment_method": "Credit Card",
            "order_url": "",
            "timestamp": round(time.time()),
            "elements": [
                {
                    "title": item['title'],
                    "quantity": 1,
                    "price": item['price'],
                    "currency": "UAH",
                    "image_url": item['image_url']
                }
                for item in items
            ],
            "summary": {
                "total_cost": total_cost
            }
        }
    }


def quick_replies_template(title, payload):
    if title == 'get_more':
        if payload.get('from') == 0:
            title = "Repeat"
            payload['type'] = 'repeat'
    template = {
        "content_type": "text",
        "title": title,
        "payload": json.dumps(payload)
    }

    return template


def quick_replies(reply_type, provider):
    return {
        'get_started': [quick_replies_template('Cafes', {'type': 'get_cafes',
                                                              'provider': provider}),
                        quick_replies_template('Checkout', {'type': 'checkout',
                                                            'provider': provider}),
                        quick_replies_template('Get Basket', {'type': 'get_basket',
                                                              'provider': provider})],

        # 'get_started': [quick_replies_template('Categories', {'type': 'get_categories',
        #                                                       'provider': provider}),
        #                 quick_replies_template('Checkout', {'type': 'checkout',
        #                                                     'provider': provider}),
        #                 quick_replies_template('Get Basket', {'type': 'get_basket',
        #                                                       'provider': provider})],

        'start_over': [quick_replies_template('Categories', {'type': 'get_categories',
                                                             'provider': provider}),
                       quick_replies_template('Checkout', {'type': 'checkout',
                                                           'provider': provider}),
                       quick_replies_template('Get Basket', {'type': 'get_basket',
                                                             'provider': provider})],

        'get_categories': [quick_replies_template('Categories', {'type': 'get_categories',
                                                                 'provider': provider}),
                           quick_replies_template('Checkout', {'type': 'checkout',
                                                               'provider': provider}),
                           quick_replies_template('Get Basket', {'type': 'get_basket',
                                                                 'provider': provider})],

        'add_product': [quick_replies_template('Categories', {'type': 'get_categories',
                                                              'provider': provider}),
                        quick_replies_template('Checkout', {'type': 'checkout',
                                                            'provider': provider}),
                        quick_replies_template('Get Basket', {'type': 'get_basket',
                                                              'provider': provider})],

        'remove_product': [quick_replies_template('Categories', {'type': 'get_categories',
                                                                 'provider': provider}),
                           quick_replies_template('Checkout', {'type': 'checkout',
                                                               'provider': provider}),
                           quick_replies_template('Get Basket', {'type': 'get_basket',
                                                                 'provider': provider})],

        'get_basket': [quick_replies_template('Categories', {'type': 'get_categories',
                                                             'provider': provider}),
                       quick_replies_template('Checkout', {'type': 'checkout',
                                                           'provider': provider}),
                       quick_replies_template('Get Basket', {'type': 'get_basket',
                                                             'provider': provider})],

        'get_category': [quick_replies_template('Checkout', {'type': 'checkout',
                                                             'provider': provider}),
                         quick_replies_template('Get Basket', {'type': 'get_basket',
                                                               'provider': provider})],
        'no_products': [quick_replies_template('Categories', {'type': 'get_categories',
                                                              'provider': provider}),
                        quick_replies_template('Checkout', {'type': 'checkout',
                                                            'provider': provider}),
                        quick_replies_template('Get Basket', {'type': 'get_basket',
                                                              'provider': provider})],
        'checkout': [quick_replies_template('Categories', {'type': 'get_categories',
                                                           'provider': provider}),
                     quick_replies_template('Get Basket', {'type': 'get_basket',
                                                           'provider': provider})],
        'receipt': [quick_replies_template('Categories', {'type': 'get_categories',
                                                          'provider': provider}),
                    quick_replies_template('Checkout', {'type': 'checkout',
                                                        'provider': provider}),
                    quick_replies_template('Get Basket', {'type': 'get_basket',
                                                          'provider': provider})],
        'unit_notify': [quick_replies_template('Categories', {'type': 'get_categories',
                                                              'provider': provider}),
                        quick_replies_template('Checkout', {'type': 'checkout',
                                                            'provider': provider}),
                        quick_replies_template('Get Basket', {'type': 'get_basket',
                                                              'provider': provider})],
        'unit_explain': [quick_replies_template('Categories', {'type': 'get_categories',
                                                               'provider': provider}),
                         quick_replies_template('Checkout', {'type': 'checkout',
                                                             'provider': provider}),
                         quick_replies_template('Get Basket', {'type': 'get_basket',
                                                               'provider': provider})],
        'unit_gift': [quick_replies_template('Categories', {'type': 'get_categories',
                                                            'provider': provider}),
                      quick_replies_template('Checkout', {'type': 'checkout',
                                                          'provider': provider}),
                      quick_replies_template('Get Basket', {'type': 'get_basket',
                                                            'provider': provider})],
        "pay_rejected": [quick_replies_template('Categories', {'type': 'get_categories',
                                                               'provider': provider}),
                         quick_replies_template('Checkout', {'type': 'checkout',
                                                             'provider': provider}),
                         quick_replies_template('Get Basket', {'type': 'get_basket',
                                                               'provider': provider})],

    }[reply_type]

import json
import time

from .constants import UNIT_REPLY_TEXT

id_types = {
    'get_categories': 'category_id',
    'get_category': 'product_id'
}

button_types = {
    'get_category': 'Add',
    'get_basket': 'Remove'
}

payloads = {
    'start_over': {'type': 'get_category'},
    'get_categories': {'type': 'get_category'},
    'get_category': {'type': 'add_product'},
    'get_basket': {'type': 'remove_product'}
}

text_types = {
    'get_started': 'Сделай заказ.',
    'add_product': 'Added.',
    'remove_product': 'Removed.',
    'start_over': UNIT_REPLY_TEXT
}


def list_template(id_type, button_type=None, *args, **kwargs):
    for arg in args:
        payload = kwargs
        payload.update({'id': arg.get('id')})
        arg.update({'payload': json.dumps(payload)})

    template = {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                {
                    "title": item.get('title'),
                    "image_url": item.get('image_url'),
                    "buttons": [
                        {
                            "title": button_type or item.get('title'),
                            "type": "postback",
                            "payload": json.dumps(item.get('payload'))
                        }
                    ]
                } for item in args]
        }
    }
    return template


def generic_template(id_type, item, button_type=None, **kwargs):
    payload = kwargs
    payload.update({'id': item.get('id')})
    item.update({'payload': payload})

    template = {
        "type": "template",
        "payload": {
            "template_type": "generic",
            "elements": [
                {
                    "title": item.get('title'),
                    "subtitle": str(item.get('price')) + ' UAH',
                    "image_url": item.get('image_url'),
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


def receipt_template(**kwargs):
    items = kwargs.get('orders')
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
        'get_started': [quick_replies_template('Categories', {'type': 'get_categories',
                                                              'provider': provider}),
                        quick_replies_template('Checkout', {'type': 'checkout',
                                                            'provider': provider})],

        'start_over': [quick_replies_template('Categories', {'type': 'get_categories',
                                                             'provider': provider}),
                       quick_replies_template('Checkout', {'type': 'checkout',
                                                           'provider': provider}),
                       quick_replies_template('Get Basket', {'type': 'get_basket',
                                                             'provider': provider})],

        'get_categories': [quick_replies_template('Checkout', {'type': 'checkout',
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
                                                           'provider': provider})],

        'get_category': [quick_replies_template('Checkout', {'type': 'checkout',
                                                             'provider': provider}),
                         quick_replies_template('Get Basket', {'type': 'get_basket',
                                                               'provider': provider})],

    }[reply_type]

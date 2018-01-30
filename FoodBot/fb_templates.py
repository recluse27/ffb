import copy
import json
import time

from .constants import (UNIT_REPLY_TEXT, SELF_URL,
                        UNIT_REPLY_EXPLAIN, UNIT_REPLY_GIFT,
                        GREETING, INSTRUCTION)

id_types = {
    'get_categories': {'self_id': 'category_id', "next_id": 'category_id'},
    'get_category': {'self_id': 'category_id', 'next_id': 'id'},
    'add_product': {'self_id': 'id', 'next_id': 'id'},
    'remove_product': {'self_id': 'id', 'next_id': 'id'},
    'get_basket': {'self_id': 'id', 'next_id': 'id'}
}

button_types = {
    'get_category': 'Додати',
    'get_basket': 'Видалити'
}

payloads = {
    'start_over': {'type': 'get_category'},
    'get_categories': {'type': 'get_category'},
    'get_category': {'type': 'add_product'},
    'get_basket': {'type': 'remove_product'}
}

link_types = {
    'checkout': SELF_URL,
}

text_types = {
    'get_started': 'Зробіть замовлення.',
    'greeting': GREETING,
    'get_instruction': INSTRUCTION,
    'add_product': 'Додано.',
    'remove_product': 'Видалено.',
    'no_products': 'У вас нема продуктів у кошику.',
    'unit_notify': UNIT_REPLY_TEXT,
    'unit_explain': UNIT_REPLY_EXPLAIN,
    'unit_gift': UNIT_REPLY_GIFT,
    'start_over': 'Зробіть замовлення.',
    "pay_rejected": "Під час оплати сталася помилка. Спробуйте ще."
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


def generic_list_template(id_type, new_items, button_type=None, **kwargs):
    items = [copy.copy(new_item) for new_item in new_items]
    payload = kwargs
    next_type = id_types.get(id_type, {}).get('next_id')
    for i in range(len(items)):
        payload.update({next_type: items[i].get(next_type)})
        items[i].update({'payload': payload})

    print("ITEMS: ", items)

    template = {
        "type": "template",
        "payload": {
            "template_type": "generic",
            "elements": [
                {
                    "title": item.get('title'),
                    "subtitle": ("{price} UAH".format(price=item.get('price')) if item.get('price') else ""),
                    "image_url": item.get('image_url', ''),
                    "buttons": [
                        {
                            "title": button_type or item.get('title'),
                            "type": "postback",
                            "payload": json.dumps(item.get('payload'))
                        }
                    ]
                } for item in items
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


QRs = {'categories': lambda provider: quick_replies_template('Категорії', {'type': 'get_categories',
                                                                           'provider': provider}),
       'payment': lambda provider: quick_replies_template('До оплати', {'type': 'checkout',
                                                                        'provider': provider}),
       'basket': lambda provider: quick_replies_template('Кошик', {'type': 'get_basket',
                                                                   'provider': provider}),
       'instruction': lambda provider: quick_replies_template('Інструкція', {'type': 'get_instruction',
                                                                        'provider': provider})
       }

method_replies = {
    'get_started': ['categories', 'payment', 'basket', 'instruction'],

    'get_instruction': ['categories', 'payment', 'basket', 'instruction'],

    'greeting': ['categories', 'payment', 'basket', 'instruction'],

    'start_over': ['categories', 'payment', 'basket', 'instruction'],

    'get_categories': ['categories', 'payment', 'basket', 'instruction'],

    'add_product': ['categories', 'payment', 'basket', 'instruction'],

    'remove_product': ['categories', 'payment', 'basket', 'instruction'],

    'get_basket': ['categories', 'payment', 'basket', 'instruction'],

    'get_category': ['payment', 'basket', 'instruction'],

    'no_products': ['categories', 'payment', 'basket', 'instruction'],

    'checkout': ['categories', 'basket', 'instruction'],

    'receipt': ['categories', 'payment', 'basket', 'instruction'],

    'unit_notify': ['categories', 'payment', 'basket', 'instruction'],

    'unit_explain': ['categories', 'payment', 'basket', 'instruction'],

    'unit_gift': ['categories', 'payment', 'basket', 'instruction'],

    "pay_rejected": ['categories', 'payment', 'basket', 'instruction'],

}


def quick_replies(reply_type, provider):
    return [QRs.get(qr_type)(provider) for qr_type in method_replies.get(reply_type, "")]

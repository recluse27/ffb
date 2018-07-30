import copy
import json
import time


def generic_list_template(new_items, button_type=None, **kwargs):
    items = [copy.copy(new_item) for new_item in new_items]
    payload = kwargs
    for item in items:
        new_payload = copy.copy(payload)
        new_payload.update({'id': item.get('id')})
        item.update({'payload': new_payload})

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
    total_cost = sum(item.get('price') for item in items)
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
                    "title": item.get('title'),
                    "quantity": 1,
                    "price": item.get('price'),
                    "currency": "UAH",
                    "image_url": item.get('image_url')
                }
                for item in items
            ],
            "summary": {
                "total_cost": total_cost
            }
        }
    }


def quick_replies_template(title, payload):
    template = {
        "content_type": "text",
        "title": title,
        "payload": json.dumps(payload)
    }

    return template


QRs = {
    'categories': lambda provider: quick_replies_template('Категорії', {'type': 'get_categories',
                                                                        'provider': provider}),
    'payment': lambda provider: quick_replies_template('До оплати', {'type': 'checkout',
                                                                     'provider': provider}),
    'basket': lambda provider: quick_replies_template('Кошик', {'type': 'get_basket',
                                                                'provider': provider}),
    'about_cafe': lambda provider: quick_replies_template('Про заклад', {'type': 'about_cafe',
                                                                         'provider': provider}),
    'cafes': lambda provider: quick_replies_template('Заклади', {'type': 'get_cafes'}),

    'instruction': lambda provider: quick_replies_template('Інструкція', {'type': 'get_instruction'}),

    'how_to_buy': lambda provider: quick_replies_template('Яким чином?', {'type': 'how_to_buy'}),

    'how_to_pay': lambda provider: quick_replies_template('Як провести оплату?', {'type': 'how_to_pay'}),

    'how_to_present': lambda provider: quick_replies_template('Як подарувати?', {'type': 'how_to_present'}),

    'how_details': lambda provider: quick_replies_template('Деталi', {'type': 'how_details'}),

    'why_bot': lambda provider: quick_replies_template('Нащо мені це?', {'type': 'why_bot'}),

    'happens': lambda provider: quick_replies_template('Трапляється', {'type': 'happens'}),

    'no_memory': lambda provider: quick_replies_template('Не пригадую', {'type': 'no_memory'}),

    'something_else': lambda provider: quick_replies_template('А що ще?', {'type': 'something_else'}),

    'something_hmm_else': lambda provider: quick_replies_template('Хмм.А що ще?', {'type': 'something_hmm_else'}),

    'yeah': lambda provider: quick_replies_template('Та да', {'type': 'yeah'}),

    'half': lambda provider: quick_replies_template('Половинка?😰', {'type': 'half'}),

    'that_is_me': lambda provider: quick_replies_template('Це про мене😄', {'type': 'that_is_me'}),

    'not_really': lambda provider: quick_replies_template('Та наче ні', {'type': 'not_really'}),
}


def quick_replies(quick_replies_list, provider):
    try:
        return [QRs.get(qr_type)(provider) for qr_type in quick_replies_list]
    except AttributeError:
        return []

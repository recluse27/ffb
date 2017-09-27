import json
import time

import requests as rq

unit_url = "https://unit.cafe/api/v1/ua/%s?token=jhy48fnc9sd"
headers = {'Content-Type': 'application/json',
           'user-agent': 'Mozilla/5.0 (Macintosh; '
                         'Intel Mac OS X 10_13_0) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/61.0.3163.100 Safari/537.36'}


def CATEGORY_LIST(CATEGORIES):
    return {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                {
                    "title": item['title'],
                    "image_url": item['image_url'],
                    "buttons": [
                        {
                            "title": item['title'],
                            "type": "postback",
                            "payload": "get_category/" + str(item['category_id'])
                        }
                    ]
                } for item in CATEGORIES]
        }
    }


def GET_CATEGORIES(categories):
    return {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                {
                    "title": item['title'],
                    "image_url": item['image_url'],
                    "buttons": [
                        {
                            "title": item['title'],
                            "type": "postback",
                            "payload": "get_category/" + str(item['category_id'])
                        }
                    ]
                } for item in categories]
        }
    }


def GET_GENERIC_CATEGORY(category):
    return {
        "type": "template",
        "payload": {
            "template_type": "generic",
            "elements": [
                {
                    "title": category['title'],
                    "image_url": category['image_url'],
                    "buttons": [
                        {
                            "title": category['title'],
                            "type": "postback",
                            "payload": "get_category/" + str(category['category_id'])
                        }
                    ]
                }
            ]
        }
    }


def GET_BASKET(items):
    return {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                {
                    "title": item['title'],
                    "subtitle": str(item['price']) + ' UAH',
                    "image_url": item['image_url'],
                    "buttons": [
                        {
                            "title": "Remove",
                            "type": "postback",
                            "payload": "remove_product/" + str(item['product_id'])
                        }]
                } for item in items]
        }
    }


def GET_GENERIC_BASKET(item):
    return {
        "type": "template",
        "payload": {
            "template_type": "generic",
            "elements": [
                {
                    "title": item['title'],
                    "subtitle": str(item['price']) + ' UAH',
                    "image_url": item['image_url'],
                    "buttons": [
                        {
                            "title": "Remove",
                            "type": "postback",
                            "payload": "remove_product/" + str(item['product_id'])
                        }
                    ]
                }
            ]
        }
    }


def PRODUCT_LIST(category, delimiter, PRODUCTS):
    filtered_items = list(filter(lambda product: str(product['category_id']) == str(category),
                                 PRODUCTS))[delimiter[0]: delimiter[1]]

    return {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                {
                    "title": item['title'],
                    "subtitle": str(item['price']) + ' UAH',
                    "image_url": item['image_url'],
                    "buttons": [
                        {
                            "title": "Add",
                            "type": "postback",
                            "payload": "add_product/" + str(item['product_id'])
                        }
                    ]
                } for item in filtered_items]
        }
    }


def GET_PRODUCTS(products):
    return {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                {
                    "title": item['title'],
                    "subtitle": str(item['price']) + ' UAH',
                    "image_url": item['image_url'],
                    "buttons": [
                        {
                            "title": "Add",
                            "type": "postback",
                            "payload": "add_product/" + str(item['product_id'])
                        }
                    ]
                } for item in products]
        }
    }


def GET_GENERIC_PRODUCT(item):
    return {
        "type": "template",
        "payload": {
            "template_type": "generic",
            "elements": [
                {
                    "title": item['title'],
                    "subtitle": str(item['price']) + ' UAH',
                    "image_url": item['image_url'],
                    "buttons": [
                        {
                            "title": "Add",
                            "type": "postback",
                            "payload": "add_product/" + str(item['product_id'])
                        }
                    ]
                }
            ]
        }
    }


def RECEIPT_TEMPLATE(items):
    return {
        "type": "template",
        "payload": {
            "template_type": "receipt",
            "recipient_name": "User",
            "order_number": round(time.time()),
            "currency": "UAH",
            "payment_method": "Credit Card",
            "order_url": "",
            "timestamp": round(time.time()),
            "elements": [
                RECEIPT_ELEMENT_TEMPLATE(item=item)
                for item in items
            ],
            "summary": {
                "total_cost": sum(item['price'] for item in items)
            }
        }
    }


def RECEIPT_ELEMENT_TEMPLATE(item):
    return {
        "title": item['title'],
        "quantity": 1,
        "price": item['price'],
        "currency": "UAH",
        "image_url": item['image_url']
    }


def QUICK_REPLIES_GET_MORE(category, _from, _to):
    return {
        "content_type": "text",
        "title": "Get more",
        "payload": "get_more/{category}/{_from}-{_to}".format(category=category,
                                                              _from=_from,
                                                              _to=_to)
    }


def BUTTONS_SHARE():
    return {
        "type": "element_share"
    }


def QUICK_REPLIES_REPEAT(category, PRODUCTS):
    filtered_products = list(filter(lambda p: str(p['category_id']) == str(category), PRODUCTS))
    return {
        "content_type": "text",
        "title": "Repeat",
        "payload": "get_more/{category}/0-{size}".format(category=category,
                                                         size=(4 if len(filtered_products) > 5
                                                               else len(filtered_products)))
    }


def QUICK_REPLIES_CATEGORIES():
    return {
        "content_type": "text",
        "title": "Categories",
        "payload": "get_categories"
    }


def QUICK_REPLIES_GET_BASKET():
    return {
        "content_type": "text",
        "title": "Get basket",
        "payload": "get_basket"
    }


def QUICK_REPLIES_CHECKOUT():
    return {
        "content_type": "text",
        "title": "Checkout",
        "payload": "checkout"
    }


def get_products():
    result = rq.get(url=(unit_url % 'product'), headers=headers)
    products = json.loads(result.text)
    new_products = [
        {'title': product.get('name'),
         'price': product.get('price'),
         'product_id': product.get('product_id'),
         'category_id': product.get('category_id'),
         'image_url': product.get('image', [{}])[0].get('image1')}
        for product in products]
    return new_products


def get_categories():
    result = rq.get(url=(unit_url % 'category'), headers=headers)
    categories = json.loads(result.text)
    new_categories = [
        {'title': category.get('name'),
         'category_id': category.get('category_id'),
         'image_url': category.get('image')}
        for category in categories
    ]
    return new_categories

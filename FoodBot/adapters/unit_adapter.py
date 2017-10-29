import json

import requests as rq

from .generic_adapter import IAdapter
from ..constants import HEADERS


class UnitAdapter(IAdapter):
    name = "Unit"
    url = "https://unit.cafe/api/v1/ua/%s?token=jhy48fnc9sd"

    def __init__(self):
        self.methods = {
            'get_categories': self.get_categories,
            'get_category': self.get_products,
            'checkout': self.checkout,
            'add_product': self.add_product,
            'remove_product': self.remove_product
        }

    def checkout(self, **kwargs):
        orders = kwargs.get('orders')
        data = {'name': 'test_user',
                'phone': kwargs.get('phone'),
                'order_time': kwargs.get('order_time'),
                'delivery_type': 1,  # in unit
                'coock_type': 2,  # all at once
                'guests_count': 1,
                'products': [{'product_id': int(product.get('product_id')),
                              'quantity': 1}
                             for product in orders]}
        result = rq.post(url=(self.url % 'order'),
                         headers=HEADERS,
                         json=data)
        return json.loads(result.text)

    def get_categories_from_api(self):
        result = rq.get(url=(self.url % 'category'), headers=HEADERS)
        categories = json.loads(result.text)
        new_categories = [
            {'title': category.get('name'),
             'id': category.get('category_id'),
             'image_url': category.get('image')}
            for category in categories
        ]
        self.cached_categories = new_categories

    def get_categories(self, **kwargs):
        if not self.cached_categories:
            self.get_categories_from_api()
        return self.cached_categories

    def get_products_from_api(self):
        result = rq.get(url=(self.url % 'product'), headers=HEADERS)
        products = json.loads(result.text)
        new_products = [
            {'title': product.get('name'),
             'price': product.get('price'),
             'id': product.get('product_id'),
             'category_id': product.get('category_id'),
             'image_url': product.get('image', [{}])[0].get('image1')}
            for product in products]
        self.cached_products = new_products

    def get_products(self, **kwargs):
        category_id = kwargs.get('category_id')
        if not self.cached_products:
            self.get_products_from_api()
        products = list(
            filter(
                lambda product: str(product['category_id']) == str(category_id),
                self.cached_products
            )
        )
        return products

    def add_product(self, **kwargs):
        if not self.cached_products:
            self.get_products_from_api()

        sender = kwargs.get('user_id')
        check = kwargs.get('orders')
        mongo = kwargs.get('mongo')
        product = list(filter(lambda p: p.get('id') == kwargs.get('id'), self.cached_products))
        print(product)
        if product:
            if check:
                mongo.db.orders.update({'userid': sender}, {"$push": {'orders': product[0]}})
            else:
                mongo.db.orders.insert({'userid': sender, 'orders': product})

    def remove_product(self, **kwargs):
        if not self.cached_products:
            self.get_products_from_api()

        sender = kwargs.get('user_id')
        orders = kwargs.get('orders')
        mongo = kwargs.get('mongo')
        product = list(filter(lambda p: p.get('id') == kwargs.get('id'), self.cached_products))
        if product:
            orders.remove(product[0])
            mongo.db.orders.update({'userid': sender}, {"$set": {'orders': orders}})

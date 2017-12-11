import json
from datetime import datetime, timedelta, timezone

import requests as rq

from .generic_adapter import IAdapter
from ..constants import HEADERS


class UnitAdapter(IAdapter):
    name = "unit"
    url = "https://unit.cafe/api/v1/ua/%s?token=aTgEy4dtnF4"

    def __init__(self):
        self.methods = {
            'get_categories': self.get_categories,
            'get_category': self.get_products,
            'checkout': self.checkout,
            'add_product': self.add_product,
            'remove_product': self.remove_product
        }

    def checkout(self, **kwargs):
        ukraine = timezone(timedelta(hours=2))
        orders = kwargs.get('orders')
        data = {'name': 'test_user',
                'phone': '38(000)444-55-66',
                'order_time': datetime.now(tz=ukraine).strftime("%Y-%m-%dT%H:%M:%S.%f"),
                'delivery_type': 1,  # in unit
                'cook_type': 2,  # all at once
                'guests_count': 1,
                'order_type': 2,
                'products': [{'product_id': int(product.get('id')),
                              'quantity': 1}
                             for product in orders]}
        result = rq.post(url=(self.url % 'order'),
                         headers=HEADERS,
                         json=data)
        print('ORDER DATA', result.text)
        return json.loads(result.text)

    def get_categories_from_api(self):
        result = rq.get(url=(self.url % 'category'), headers=HEADERS)
        categories = json.loads(result.text)
        new_categories = [
            {'title': category.get('name'),
             'category_id': category.get('category_id'),
             'image_url': category.get('image')}
            for category in categories
        ]
        self.cached_categories = new_categories
        self.cached_categories_updated = datetime.utcnow()

    def get_categories(self, **kwargs):
        if not self.cached_categories:  # or (self.cached_categories_updated + timedelta(days=CACHE_UPDATE_DAYS) < datetime.utcnow()):
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
        self.cached_products_updated = datetime.utcnow()

    def get_products(self, **kwargs):
        category_id = kwargs.get('category_id')
        if not self.cached_products:  # or (self.cached_products_updated + timedelta(days=CACHE_UPDATE_DAYS) < datetime.utcnow()):
            self.get_products_from_api()
        products = list(
            filter(
                lambda product: str(product['category_id']) == str(category_id),
                self.cached_products
            )
        )
        return products

    def is_product_available(self, product_id):
        result = rq.get(url=(self.url % 'product/{id}'.format(id=product_id)),
                        headers=HEADERS)
        try:
            product_data = json.loads(result.text)[0]
            print('NO ERROR')
            return bool(product_data.get('status'))
        except:
            print('ERROR')
            return False

    def add_product(self, **kwargs):
        if not self.cached_products:
            self.get_products_from_api()

        sender = kwargs.get('user_id')
        check = kwargs.get('orders')
        mongo = kwargs.get('mongo')
        provider = kwargs.get('provider')
        if not check:
            mongo.orders.remove({"userid": sender, "provider": provider})
            check = None

        product = list(filter(lambda p: p.get('id') == kwargs.get('id'), self.cached_products))
        print("ID", kwargs.get('id'))
        if not self.is_product_available(kwargs.get('id')):
            return "Продукт наразі недоступний."

        if product:
            print("PRODUCT", product)
            if 'payload' in product[0]:
                product[0].pop('payload')
            if check:
                mongo.orders.update({'userid': sender, 'provider': provider}, {"$push": {'orders': product[0]}})
            else:
                mongo.orders.insert({'userid': sender, 'orders': product, 'provider': provider})

    def remove_product(self, **kwargs):
        if not self.cached_products:
            self.get_products_from_api()

        sender = kwargs.get('user_id')
        orders = kwargs.get('orders')
        mongo = kwargs.get('mongo')
        provider = kwargs.get('provider')
        product = list(filter(lambda p: p.get('id') == kwargs.get('id'), self.cached_products))
        print("PRODUCT", product)
        if product:
            if 'payload' in product[0]:
                product[0].pop('payload')
            orders.remove(product[0])
            mongo.orders.update({'userid': sender, 'provider': provider}, {"$set": {'orders': orders}})

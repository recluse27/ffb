import json
from datetime import datetime, timedelta, timezone

import requests as rq

from FoodBot.adapters.generic_adapter import IAdapter
from FoodBot.constants import HEADERS, CACHE_UPDATE_DAYS
from FoodBot.models import Product, Category, BotOrder
from FoodBot.utils import get_or_create_order


class UnitAdapter(IAdapter):
    testing = False
    image_url = "https://apply.unit.ua/assets/img/logo.png?v043"
    provider_name = "unit"
    name = "UnitCafe"
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

        data = {'name': 'user',
                'phone': '38(000)444-55-66',
                'order_time': datetime.now(tz=ukraine).strftime("%Y-%m-%dT%H:%M:%S.%f"),
                'delivery_type': 1,  # in unit
                'cook_type': 2,  # all at once
                'guests_count': 1,
                'order_type': 2,
                'products': [{'product_id': product.get('id'),
                              'quantity': 1}
                             for product in orders]}

        result = rq.post(url=(self.url % 'order'),
                         headers=HEADERS,
                         json=data)

        return json.loads(result.text)

    def get_categories_from_api(self):
        result = rq.get(url=(self.url % 'facebookcategory'), headers=HEADERS)
        categories = json.loads(result.text)
        new_categories = [
            Category(**{'title': category.get('name'),
                        'category_id': category.get('category_id'),
                        'image_url': category.get('image')})
            for category in categories
        ]
        self.cached_categories = new_categories
        self.cached_categories_updated = datetime.utcnow()

    def get_products_from_api(self):
        result = rq.get(url=(self.url % 'product'), headers=HEADERS)
        products = json.loads(result.text)

        new_products = [
            Product(**{'title': product.get('name'),
                       'price': product.get('price'),
                       'id': product.get('product_id'),
                       'category_id': product.get('facebook_category') or product.get('category_id'),
                       'image_url': product.get('image', [{}])[0].get('image1')})
            for product in products]

        self.cached_products = new_products
        self.cached_products_updated = datetime.utcnow()

    def get_categories(self, **kwargs):
        expire_date = self.cached_categories_updated + timedelta(days=CACHE_UPDATE_DAYS)

        if not self.cached_categories or (expire_date < datetime.utcnow()):
            self.get_categories_from_api()

        categories = [category.to_json() for category in self.cached_categories]

        return categories

    def get_products(self, **kwargs):
        expire_date = self.cached_categories_updated + timedelta(days=CACHE_UPDATE_DAYS)
        category_id = kwargs.get('id')
        if not self.cached_products or (expire_date < datetime.utcnow()):
            self.get_products_from_api()

        products = [product.to_json() for product in self.cached_products if product.category_id == category_id]

        return products

    def get_product_by_id(self, id):
        expire_date = self.cached_categories_updated + timedelta(days=CACHE_UPDATE_DAYS)
        if not self.cached_products or (expire_date < datetime.utcnow()):
            self.get_products_from_api()

        result = list(filter(lambda product: product.id == id, self.cached_products))
        return result[0] if result else None

    def is_product_available(self, product_id):
        result = rq.get(url=(self.url % 'product/{id}'.format(id=product_id)),
                        headers=HEADERS)
        try:
            product_data = json.loads(result.text)[0]
            return bool(product_data.get('status'))
        except TypeError:
            return False

    def add_product(self, **kwargs):
        if not self.cached_products:
            self.get_products_from_api()

        sender = kwargs.get('user_id')
        provider = kwargs.get('provider')
        product_id = kwargs.get('id')
        user_order = get_or_create_order(BotOrder, sender, provider)

        product = self.get_product_by_id(product_id)
        if not self.is_product_available(product_id) or product is None:
            return "Продукт наразі недоступний."

        orders = user_order.orders
        orders.append(product.to_json())
        user_order.orders = orders
        user_order.save()
        return "Додано {title}.".format(title=product.title)

    def remove_product(self, **kwargs):
        if not self.cached_products:
            self.get_products_from_api()

        sender = kwargs.get('user_id')
        provider = kwargs.get('provider')
        product_id = kwargs.get('id')
        user_order = get_or_create_order(BotOrder, sender, provider)

        product = self.get_product_by_id(product_id)
        if product is None:
            return "Продукт наразі недоступний."

        orders = user_order.orders
        orders.remove(product.to_json())
        user_order.orders = orders
        user_order.save()
        return "Видалено {title}.".format(title=product.title)

import json
from datetime import datetime, timedelta, timezone

import requests as rq

from FoodBot.adapters.generic_adapter import IAdapter
from FoodBot.constants import HEADERS
from FoodBot.models import Product, Category


class DruziAdapter(IAdapter):
    image_url = "http://druzicafe.com.ua/wp-includes/img/logo.png"
    provider_name = "druzi"
    name = "DruziCafe"
    url = "https://cafesystem.herokuapp.com/bot/cafes/druzi/"

    def is_product_available(self, product_id) -> bool:
        return True

    def checkout(self, **kwargs) -> dict:
        ukraine = timezone(timedelta(hours=2))
        orders = kwargs.get('orders')

        data = {'user_id': kwargs.get('user_id'),
                'order_time': datetime.now(tz=ukraine).strftime("%Y-%m-%dT%H:%M:%S.%f"),
                'orders': [product.get('id') for product in orders]}

        result = rq.post(url=(self.url + 'checkout/'),
                         headers=HEADERS,
                         json=data)

        return json.loads(result.text).get('order')

    def get_categories_from_api(self) -> None:
        result = rq.get(url=(self.url + "categories/"), headers=HEADERS)
        categories = json.loads(result.text)
        new_categories = [
            Category(**{'title': category.get('name'),
                        'category_id': category.get('id'),
                        'image_url': category.get('image_url')})
            for category in categories.get('categories')
        ]
        self.cached_categories = new_categories
        self.cached_categories_updated = datetime.utcnow()

    def get_products_from_api(self) -> None:
        result = rq.get(url=(self.url + 'products/'), headers=HEADERS)
        products = json.loads(result.text)

        new_products = [
            Product(**{'title': product.get('name'),
                       'price': product.get('price'),
                       'id': product.get('id'),
                       'category_id': product.get('category'),
                       'image_url': product.get('image_url')})
            for product in products.get('products')]

        self.cached_products = new_products
        self.cached_products_updated = datetime.utcnow()

import json
from datetime import datetime, timedelta, timezone

import requests as rq

from FoodBot.adapters.generic_adapter import IAdapter
from FoodBot.constants import HEADERS
from FoodBot.models import Product, Category


class UnitAdapter(IAdapter):
    image_url = "https://apply.unit.ua/assets/img/logo.png?v043"
    provider_name = "unit"
    name = "UnitCafe"
    url = "https://unit.cafe/api/v1/ua/%s?token=aTgEy4dtnF4"

    def checkout(self, **kwargs) -> dict:
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

    def get_categories_from_api(self) -> None:
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

    def get_products_from_api(self) -> None:
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

    def is_product_available(self, product_id) -> bool:
        result = rq.get(url=(self.url % 'product/{id}'.format(id=product_id)),
                        headers=HEADERS)
        try:
            product_data = json.loads(result.text)[0]
            return bool(product_data.get('status'))
        except TypeError:
            return False
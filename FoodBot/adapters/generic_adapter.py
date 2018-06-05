import json
from datetime import datetime, timedelta, timezone
from typing import Optional, List

import requests as rq

from FoodBot.constants import CACHE_UPDATE_DAYS, HEADERS, CAFE_SYSTEM_URL
from FoodBot.models import Product, BotOrder, Category, Cafe
from FoodBot.utils import get_or_create_order


class GenericAdapter:
    cafe = None
    name = None
    url = None
    image_url = None
    provider_name = None

    cached_products = []
    cached_categories = []
    cached_categories_updated = None
    cached_products_updated = None

    def __init__(self, cafe: Cafe):
        self.cafe = cafe
        self.name = cafe.name
        self.image_url = cafe.image_url
        self.provider_name = cafe.provider_name
        self.url = CAFE_SYSTEM_URL + "bot/cafes/{name}/".format(name=cafe.provider_name)

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

    def is_product_available(self, product_id) -> bool:
        return True

    def get_categories(self, **kwargs) -> List[dict]:
        expire_date = (self.cached_categories_updated + timedelta(days=CACHE_UPDATE_DAYS)
                       if self.cached_categories_updated else None)

        if not self.cached_categories or (expire_date and expire_date < datetime.utcnow()):
            self.get_categories_from_api()

        categories = [category.to_json() for category in self.cached_categories]

        return categories

    def get_products(self, **kwargs) -> List[dict]:
        expire_date = (self.cached_products_updated + timedelta(days=CACHE_UPDATE_DAYS)
                       if self.cached_products_updated else None)
        category_id = kwargs.get('id')
        if not self.cached_products or (expire_date and expire_date < datetime.utcnow()):
            self.get_products_from_api()

        products = [product.to_json() for product in self.cached_products if product.category_id == category_id]

        return products

    def get_product_by_id(self, product_id) -> Optional[Product]:
        expire_date = (self.cached_products_updated + timedelta(days=CACHE_UPDATE_DAYS)
                       if self.cached_products_updated else None)

        if not self.cached_products or (expire_date and expire_date < datetime.utcnow()):
            self.get_products_from_api()

        result = list(filter(lambda product: product.id == product_id, self.cached_products))
        return result[0] if result else None

    def add_product(self, **kwargs) -> str:
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
        user_order.commit()
        return "Додано {title}.".format(title=product.title)

    def remove_product(self, **kwargs) -> str:
        if not self.cached_products:
            self.get_products_from_api()

        sender = kwargs.get('user_id')
        provider = kwargs.get('provider')
        product_id = kwargs.get('id')
        user_order = get_or_create_order(BotOrder, sender, provider)

        product = self.get_product_by_id(product_id)
        orders = user_order.orders
        product_json = {}
        if product is None:
            for actual_product in orders:
                if actual_product.get('id') == product_id:
                    product_json = actual_product

        else:
            product_json = product.to_json()

        orders.remove(product_json)
        user_order.orders = orders
        user_order.commit()
        return "Видалено {title}.".format(title=product_json.get('title'))

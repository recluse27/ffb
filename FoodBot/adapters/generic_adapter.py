import json
from datetime import datetime, timedelta
from typing import Optional, List

import requests as rq

from FoodBot.constants import CACHE_UPDATE_DAYS, HEADERS
from FoodBot.models import Product, BotOrder
from FoodBot.utils import get_or_create_order


class IAdapter:
    name = None
    url = None
    image_url = None
    provider_name = None

    cached_products = []
    cached_categories = []
    cached_categories_updated = None
    cached_products_updated = None

    def get_categories_from_api(self) -> None:
        raise NotImplementedError

    def get_products_from_api(self) -> None:
        raise NotImplementedError

    def checkout(self, **kwargs) -> dict:
        raise NotImplementedError

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

    def is_product_available(self, product_id) -> bool:
        result = rq.get(url=(self.url % 'product/{id}'.format(id=product_id)),
                        headers=HEADERS)
        try:
            product_data = json.loads(result.text)[0]
            return bool(product_data.get('status'))
        except TypeError:
            return False

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
        if product is None:
            return "Продукт наразі недоступний."

        orders = user_order.orders
        orders.remove(product.to_json())
        user_order.orders = orders
        user_order.commit()
        return "Видалено {title}.".format(title=product.title)

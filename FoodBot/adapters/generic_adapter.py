from FoodBot.models import Product
from typing import Optional, List


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

    def add_product(self, **kwargs) -> str:
        raise NotImplementedError

    def get_product_by_id(self, id) -> Optional(Product):
        raise NotImplementedError

    def remove_product(self, **kwargs) -> str:
        raise NotImplementedError

    def get_products(self, **kwargs) -> List(dict):
        raise NotImplementedError

    def get_categories(self, **kwargs) -> List(dict):
        raise NotImplementedError

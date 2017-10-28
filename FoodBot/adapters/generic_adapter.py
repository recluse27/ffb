class IAdapter:
    name = None
    url = None
    methods = []
    cached_products = []
    cached_categories = []

    def get_categories_from_api(self):
        raise NotImplementedError

    def get_products_from_api(self):
        raise NotImplementedError

    def checkout(self, **kwargs):
        raise NotImplementedError

    def add_product(self, **kwargs):
        raise NotImplementedError

    def remove_product(self, **kwargs):
        raise NotImplementedError

    def get_products(self, **kwargs):
        raise NotImplementedError

    def get_categories(self, **kwargs):
        raise NotImplementedError

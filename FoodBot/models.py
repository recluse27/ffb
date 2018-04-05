import requests as rq
from umongo import Document, fields, Instance

from FoodBot import mongo, testing

client = mongo
db = client.heroku_dx30fc17 if not testing else client.heroku_xrfxrbss
instance = Instance(db)


@instance.register
class BotOrder(Document):
    user_id = fields.StrField()
    provider = fields.StrField()
    orders = fields.ListField(fields.DictField, required=False, default=[])


@instance.register
class CafeOrder(Document):
    user_id = fields.StrField()
    provider = fields.StrField()
    confirm_code = fields.StrField()
    order_id = fields.StrField()
    order_time = fields.StrField()
    cook_time = fields.StrField()
    special_price = fields.IntField()
    price = fields.IntField()
    order_code = fields.StrField()
    bot_order = fields.ObjectIdField()


class Message:
    def __init__(self, message_data, user_id, quick_replies=None, message_type="text"):
        self.message_type = message_type
        self.message_data = message_data
        self.quick_replies = quick_replies
        self.user_id = user_id

    def send(self, url):
        message = {"recipient": {"id": self.user_id},
                   "message": {self.message_type: self.message_data,
                               "quick_replies": self.quick_replies}}

        response = rq.post(url=url, json=message)
        print(message)
        print(response.text)
        return response


class Cafe:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.provider_name = kwargs.get("provider_name")
        self.payment_type = kwargs.get("payment_type")
        self.address = kwargs.get("address")
        self.info = kwargs.get("info")
        self.image_url = kwargs.get("image_url")
        self.testing = False


class Product:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.price = kwargs.get('price')
        self.id = kwargs.get('id')
        self.category_id = kwargs.get('category_id')
        self.image_url = kwargs.get('image_url')

    def to_json(self):
        return {'title': self.title,
                'price': self.price,
                'id': self.id,
                'category_id': self.category_id,
                'image_url': self.image_url}


class Category:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.id = kwargs.get('category_id')
        self.image_url = kwargs.get('image_url')

    def to_json(self):
        return {'title': self.title,
                'id': self.id,
                'image_url': self.image_url}

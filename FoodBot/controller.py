import json
from datetime import datetime, timezone, timedelta
from typing import List

import requests as rq

from FoodBot.adapters import GenericAdapter
from FoodBot.constants import (GREETING, REPLY_EXPLAIN, REPLY_GIFT, CAFE_SYSTEM_URL,
                               TEXT, ATTACHMENT, INSTRUCTION_PART_1,
                               INSTRUCTION_PART_2, INSTRUCTION_PART_3,
                               INSTRUCTION_PART_4, INSTRUCTION_PART_5)
from FoodBot.fb_templates import (generic_link_template, generic_list_template,
                                  receipt_template, quick_replies)
from FoodBot.models import Message, BotOrder, CafeOrder, Cafe
from FoodBot.utils import transform, require_provider, get_or_create_order, rework_checkout_data


class Controller:
    cafe_system_url = CAFE_SYSTEM_URL
    adapters = {
    }

    def __init__(self):
        self.get_cafes("Loader")

    @staticmethod
    def is_response_valid(data) -> bool:
        if (not data or
                any([item in data for item in ['delivery', 'read']]) or
                'is_echo' in data.get('message', {})):
            return False

        return True

    @staticmethod
    def get_message_payload(data) -> dict:
        payload = None
        if data.get('message', {}).get('quick_reply'):
            payload = data.get('message', {}).get('quick_reply', {}).get('payload')
        elif 'postback' in data:
            payload = data.get('postback', {}).get('payload')
        try:
            payload = json.loads(payload)
        except (ValueError, TypeError):
            payload = {'type': 'get_cafes'}
        return payload

    @staticmethod
    def get_sender(data) -> str:
        return data.get('sender').get('id')

    def handle_message(self, data) -> List[Message]:
        sender = self.get_sender(data)
        payload = self.get_message_payload(data)
        payload.update({"user_id": sender})
        method = payload.get("type")
        print(method.upper())
        return self.__getattribute__(method)(sender, **payload)

    def get_started(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               kwargs.get('provider', 'unit'))

        message = Message(user_id=sender,
                          message_type=TEXT,
                          message_data='Зробіть замовлення.',
                          quick_replies=quick_replies_instance)
        return [message]

    def greeting(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)

        rq.post(url=self.cafe_system_url + "bot/users/",
                json={'user_id': sender})

        message = Message(user_id=sender,
                          message_type=TEXT,
                          message_data=GREETING,
                          quick_replies=quick_replies_instance)
        return [message]

    def get_instruction(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=INSTRUCTION_PART_1,
                    quick_replies=quick_replies_instance),
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=INSTRUCTION_PART_2,
                    quick_replies=quick_replies_instance),
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=INSTRUCTION_PART_3,
                    quick_replies=quick_replies_instance),
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=INSTRUCTION_PART_4,
                    quick_replies=quick_replies_instance),
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=INSTRUCTION_PART_5,
                    quick_replies=quick_replies_instance),

        ]
        return messages

    def get_product(self, sender, **kwargs) -> List[Message]:
        quick_replies_instance = {}
        message = Message(user_id=sender,
                          message_type="",
                          message_data="",
                          quick_replies=quick_replies_instance)
        return [message]

    def get_cafes(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        result = rq.get(self.cafe_system_url + "bot/cafes/")

        cafes_list = json.loads(result.text).get("cafes")
        for cafe in cafes_list:
            cafe_model = Cafe(**cafe)
            adapter = GenericAdapter(cafe_model)
            self.adapters[cafe.get("provider_name")] = adapter

        cafes = [{'title': cafe_value.name,
                  'id': cafe_key,
                  'image_url': cafe_value.image_url} for cafe_key, cafe_value in self.adapters.items()]
        rearranged_cafes = transform(cafes)

        messages = []
        for cafe_list in rearranged_cafes:
            messages.append(Message(user_id=sender,
                                    message_type=ATTACHMENT,
                                    message_data=generic_list_template(cafe_list,
                                                                       **{'type': 'get_cafe'}),
                                    quick_replies=quick_replies_instance))
        return messages

    def get_cafe(self, sender, **kwargs) -> List[Message]:
        provider = kwargs.get('id')
        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)
        message = Message(user_id=sender,
                          message_type=TEXT,
                          message_data='Чудовий вибір!🙂 '
                                       'Тепер час обрати подаруночок🎁! '
                                       'Натисніть «Категорії», щоб обрати '
                                       'необхідну позицію у меню😉',
                          quick_replies=quick_replies_instance)
        return [message]

    def pay_rejected(self, **kwargs) -> List[Message]:
        cafe_order = CafeOrder.find_one({"order_id": kwargs.get('order_id')})
        if cafe_order is None:
            return []

        sender = cafe_order.user_id
        quick_replies_list = ['cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               cafe_order.provider)
        return [Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Під час оплати сталася помилка. Спробуйте ще.",
                        quick_replies=quick_replies_instance)]

    def notify(self, **kwargs) -> List[Message]:
        cafe_order = CafeOrder.find_one({"order_id": kwargs.get('order_id'),
                                         "provider": kwargs.get("provider")})
        if cafe_order is None:
            return []

        ukraine = timezone(timedelta(hours=2))
        provider = kwargs.get('provider')
        adapter = self.adapters.get(provider)
        order_time = (datetime.now(tz=ukraine) + timedelta(days=adapter.cafe.days_expire)).strftime("%d-%m-%Y")
        text_data = {"date": order_time,
                     "cafe_name": adapter.cafe.name}

        sender = cafe_order.user_id
        bot_order = get_or_create_order(BotOrder, cafe_order.user_id, cafe_order.provider)
        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               cafe_order.provider)

        cafe_order_data = cafe_order.dump()
        bot_order_data = bot_order.dump()
        cafe_order_data.update(text_data)
        bot_order_data.update(text_data)

        messages = [
            Message(user_id=sender,
                    message_type=ATTACHMENT,
                    message_data=receipt_template(**bot_order_data),
                    quick_replies=quick_replies_instance),
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=REPLY_EXPLAIN(**cafe_order_data),
                    quick_replies=quick_replies_instance),
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=REPLY_GIFT(**cafe_order_data),
                    quick_replies=quick_replies_instance)
        ]

        bot_order.orders = []
        bot_order.commit()
        return messages

    @require_provider
    def add_product(self, sender, **kwargs) -> List[Message]:
        provider = kwargs.get('provider')
        adapter = self.adapters.get(provider)

        result = adapter.add_product(**kwargs)
        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        message = Message(user_id=sender,
                          message_type=TEXT,
                          message_data=result,
                          quick_replies=quick_replies_instance)
        return [message]

    @require_provider
    def remove_product(self, sender, **kwargs) -> List[Message]:
        provider = kwargs.get('provider')
        adapter = self.adapters.get(provider)

        result = adapter.remove_product(**kwargs)
        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        message = Message(user_id=sender,
                          message_type=TEXT,
                          message_data=result,
                          quick_replies=quick_replies_instance)
        return [message]

    @require_provider
    def get_categories(self, sender, **kwargs) -> List[Message]:
        provider = kwargs.get('provider')
        adapter = self.adapters.get(provider)

        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        result = adapter.get_categories(**kwargs)
        rearranged_categories = transform(result)

        messages = []
        for category_list in rearranged_categories:
            messages.append(Message(user_id=sender,
                                    message_type=ATTACHMENT,
                                    message_data=generic_list_template(category_list, **{'provider': provider,
                                                                                         'type': 'get_category'}),
                                    quick_replies=quick_replies_instance))
        return messages

    @require_provider
    def get_category(self, sender, **kwargs) -> List[Message]:
        provider = kwargs.get('provider')
        adapter = self.adapters.get(provider)

        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        result = adapter.get_products(**kwargs)
        if not result:
            return [Message(user_id=sender,
                            message_type=TEXT,
                            message_data="У цій категорії нема продуктів.",
                            quick_replies=quick_replies_instance)]

        rearranged_products = transform(result)

        messages = []
        for product_list in rearranged_products:
            messages.append(Message(user_id=sender,
                                    message_type=ATTACHMENT,
                                    message_data=generic_list_template(product_list, 'Додати', **{'provider': provider,
                                                                                                  'type': 'add_product'}),
                                    quick_replies=quick_replies_instance))
        return messages

    @require_provider
    def get_basket(self, sender, **kwargs) -> List[Message]:
        provider = kwargs.get('provider')
        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        order = BotOrder.find_one({"user_id": sender,
                                   "provider": provider})

        if order is None or not order.orders:
            return [Message(user_id=sender,
                            message_type=TEXT,
                            message_data='У вас нема продуктів у кошику.',
                            quick_replies=quick_replies_instance)]

        messages = []
        rearranged_products = transform(order.orders)
        for product_list in rearranged_products:
            messages.append(Message(user_id=sender,
                                    message_type=ATTACHMENT,
                                    message_data=generic_list_template(product_list, 'Видалити',
                                                                       **{'provider': provider,
                                                                          'type': 'remove_product'}),
                                    quick_replies=quick_replies_instance))
        return messages

    @require_provider
    def checkout(self, sender, **kwargs) -> List[Message]:
        provider = kwargs.get('provider')
        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        adapter = self.adapters.get(provider)

        bot_order = BotOrder.find_one({"user_id": sender,
                                       "provider": provider})

        if bot_order is None or not bot_order.orders:
            return [Message(user_id=sender,
                            message_type=TEXT,
                            message_data='У вас нема продуктів у кошику.',
                            quick_replies=quick_replies_instance)]

        data_to_checkout = bot_order.dump()
        data_to_checkout.update({"user_id": sender})

        result = adapter.checkout(**data_to_checkout)
        rework_checkout_data(result, **{"user_id": sender,
                                        "provider": provider,
                                        "bot_order": bot_order.pk})

        cafe_order = CafeOrder(**result)
        cafe_order.commit()
        if adapter.cafe.testing:
            data_to_show = cafe_order.dump()
            data_to_show.update({"date": str(datetime.now().date()),
                                 "cafe_name": adapter.name})
            messages = [
                Message(user_id=sender,
                        message_type=ATTACHMENT,
                        message_data=receipt_template(**bot_order.dump()),
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data=REPLY_EXPLAIN(**data_to_show),
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data=REPLY_GIFT(**data_to_show),
                        quick_replies=quick_replies_instance)
            ]
            cafe_order.delete()
            bot_order.orders = []
            bot_order.commit()
            return messages

        url = '{url}/payments/{name}/{order_id}/'
        url = url.format(url=self.cafe_system_url,
                         name=adapter.cafe.provider_name,
                         order_id=result.get("order_id"))

        message = Message(user_id=sender,
                          message_type=ATTACHMENT,
                          message_data=generic_link_template(url, 'Будь ласка, здійсніть оплату.'),
                          quick_replies=quick_replies_instance)
        return [message]

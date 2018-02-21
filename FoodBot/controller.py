import json

from FoodBot.adapters.unit_adapter import UnitAdapter
from FoodBot.constants import (GREETING, INSTRUCTION, SELF_URL, REPLY_TEXT, REPLY_EXPLAIN, REPLY_GIFT,
                               TEXT, ATTACHMENT)
from FoodBot.fb_templates import (generic_link_template, generic_list_template,
                                  receipt_template, quick_replies)
from FoodBot.models import Message, BotOrder, CafeOrder
from FoodBot.utils import transform, require_provider, get_or_create_order


class Controller:
    adapters = {
        'unit': UnitAdapter()
    }

    @staticmethod
    def is_response_valid(data):
        if (not data or
                any([item in data for item in ['delivery', 'echo']]) or
                    'is_echo' in data.get('message', {})):
            return False

        return False

    @staticmethod
    def get_message_payload(data):
        payload = None
        print(data)
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
    def get_sender(data):
        return data.get('sender').get('id')

    def handle_message(self, data):
        sender = self.get_sender(data)
        payload = self.get_message_payload(data)
        method = payload.get("type")
        return self.__getattribute__(method)(sender, **payload)

    def get_started(self, sender, **kwargs):
        quick_replies_list = ['cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               kwargs.get('provider', 'unit'))
        message = Message(user_id=sender,
                          message_type=TEXT,
                          message_data='Зробіть замовлення.',
                          quick_replies=quick_replies_instance)
        return [message]

    def greeting(self, sender, **kwargs):
        quick_replies_list = ['cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        message = Message(user_id=sender,
                          message_type=TEXT,
                          message_data=GREETING,
                          quick_replies=quick_replies_instance)
        return [message]

    def get_instruction(self, sender, **kwargs):
        quick_replies_list = ['cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        message = Message(user_id=sender,
                          message_type=TEXT,
                          message_data=INSTRUCTION,
                          quick_replies=quick_replies_instance)
        return [message]

    @require_provider
    def add_product(self, sender, provider, **kwargs):
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
    def remove_product(self, sender, provider, **kwargs):
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

    def unit_notify(self, **kwargs):
        cafe_order = CafeOrder.find_one({"order_id": kwargs.get('order_id')})
        if cafe_order is None:
            return []

        sender = cafe_order.user_id
        bot_order = get_or_create_order(BotOrder, cafe_order.user_id, cafe_order.provider)
        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               cafe_order.provider)
        return [
            Message(user_id=sender,
                    message_type=ATTACHMENT,
                    message_data=receipt_template(**bot_order.to_json()),
                    quick_replies=quick_replies_instance),
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=REPLY_EXPLAIN(**cafe_order.dump()),
                    quick_replies=quick_replies_instance),
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=REPLY_GIFT(**cafe_order.dump()),
                    quick_replies=quick_replies_instance),

        ]

    @require_provider
    def get_categories(self, sender, **kwargs):
        provider = kwargs.get('provider')
        adapter = self.adapters.get(provider)

        result = adapter.get_categories(**kwargs)
        rearranged_categories = transform(result)
        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        messages = []
        for category_list in rearranged_categories:
            messages.append(Message(user_id=sender,
                                    message_type=ATTACHMENT,
                                    message_data=generic_list_template(category_list, **{'provider': provider,
                                                                                       'type': 'get_category'}),
                                    quick_replies=quick_replies_instance))
        return messages

    @require_provider
    def get_category(self, sender, provider, **kwargs):
        adapter = self.adapters.get(provider)

        result = adapter.get_products(**kwargs)
        rearranged_products = transform(result)
        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        messages = []
        for product_list in rearranged_products:
            messages.append(Message(user_id=sender,
                                    message_type=ATTACHMENT,
                                    message_data=generic_list_template(product_list, **{'provider': provider,
                                                                                      'type': 'get_product'}),
                                    quick_replies=quick_replies_instance))
        return messages

    @require_provider
    def get_basket(self, sender, provider, **kwargs):
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
                                    message_data=generic_list_template(product_list, **{'provider': provider,
                                                                                      'type': 'get_product'}),
                                    quick_replies=quick_replies_instance))
        return messages

    @require_provider
    def checkout(self, sender, provider, **kwargs):
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

        result = adapter.checkout(**bot_order.dump())
        result.update({"user_id": sender,
                       "provider": provider,
                       "bot_order": bot_order.pk})

        cafe_order = CafeOrder(**result)
        cafe_order.commit()
        if adapter.testing:
            return [
                Message(user_id=sender,
                        message_type=ATTACHMENT,
                        message_data=receipt_template(**bot_order.to_json()),
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data=REPLY_TEXT(**cafe_order.dump()),
                        quick_replies=quick_replies_instance)
            ]

        url = SELF_URL + '/order/' + str(cafe_order.order_id)

        message = Message(user_id=sender,
                          message_type=ATTACHMENT,
                          message_data=generic_link_template(url, 'Будь ласка, здійсніть оплату.'),
                          quick_replies=quick_replies_instance)
        return [message]

    def get_product(self, sender, **kwargs):
        quick_replies_instance = {}
        message = Message(user_id=sender,
                          message_type="",
                          message_data="",
                          quick_replies=quick_replies_instance)
        pass

    def get_cafes(self, sender, **kwargs):
        quick_replies_list = ['cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
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

    def get_cafe(self, sender, **kwargs):
        provider = kwargs.get('id')
        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)
        message = Message(user_id=sender,
                          message_type=TEXT,
                          message_data='Зробіть замовлення.',
                          quick_replies=quick_replies_instance)
        return [message]

    def pay_rejected(self, **kwargs):
        cafe_order = CafeOrder.find_one({"order_id": kwargs.get('order_id')})
        if cafe_order is None:
            return []

        sender = cafe_order.user_id
        quick_replies_list = ['categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               cafe_order.provider)
        return [Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Під час оплати сталася помилка. Спробуйте ще.",
                        quick_replies=quick_replies_instance)]

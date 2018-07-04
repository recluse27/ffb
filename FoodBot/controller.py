import json
from datetime import datetime, timezone, timedelta
from typing import List

import requests as rq

from FoodBot.adapters import GenericAdapter
from FoodBot.constants import (REPLY_EXPLAIN, REPLY_GIFT, CAFE_SYSTEM_URL,
                               TEXT, ATTACHMENT, INSTRUCTION, GREETING,
                               WHY_BOT)
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
        print(payload)
        print(self.adapters.keys())
        print(method.upper())
        return self.__getattribute__(method)(sender, **payload)

    def get_started(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['why_bot', 'cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               kwargs.get('provider', 'unit'))

        message = Message(user_id=sender,
                          message_type=TEXT,
                          message_data='Зробіть замовлення.',
                          quick_replies=quick_replies_instance)
        return [message]

    def greeting(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['why_bot', 'cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)

        rq.post(url=self.cafe_system_url + "bot/users/",
                json={'user_id': sender})

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=text,
                    timeout=1,
                    quick_replies=quick_replies_instance) for text in GREETING
        ]
        return messages

    def get_instruction(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['how_to_buy']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        texts = INSTRUCTION.get("initial")

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=text,
                    timeout=1,
                    quick_replies=quick_replies_instance) for text in texts
        ]
        return messages

    def how_to_buy(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['how_to_pay']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        texts = INSTRUCTION.get("how_to_buy")

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=text,
                    timeout=1,
                    quick_replies=quick_replies_instance) for text in texts
        ]
        return messages

    def how_to_pay(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['how_to_present']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        texts = INSTRUCTION.get("how_to_pay")

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=text,
                    timeout=1,
                    quick_replies=quick_replies_instance) for text in texts
        ]
        return messages

    def how_to_present(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['how_details']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        texts = INSTRUCTION.get("how_to_present")

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=text,
                    timeout=1,
                    quick_replies=quick_replies_instance) for text in texts
        ]
        return messages

    def how_details(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['why_bot', 'cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        texts = INSTRUCTION.get("how_details")

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=text,
                    timeout=1,
                    quick_replies=quick_replies_instance) for text in texts
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
        quick_replies_list = ['why_bot', 'cafes']
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

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data="Щоб обрати заклад - натисніть на його назву.",
                    quick_replies=quick_replies_instance),
        ]
        for cafe_list in rearranged_cafes:
            messages.append(Message(user_id=sender,
                                    message_type=ATTACHMENT,
                                    message_data=generic_list_template(cafe_list,
                                                                       **{'type': 'get_cafe'}),
                                    quick_replies=quick_replies_instance))
        return messages

    def get_cafe(self, sender, **kwargs) -> List[Message]:
        provider = kwargs.get('id')
        quick_replies_list = ['why_bot', 'categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        kwargs['provider'] = provider
        adapter = self.adapters.get(provider)

        result = adapter.get_categories(**kwargs)
        rearranged_categories = transform(result)

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data='Чудовий вибір!🙂 '
                                 'Щоб обрати категорію меню - натисніть на її назву.😉',
                    quick_replies=quick_replies_instance)
        ]
        for category_list in rearranged_categories:
            messages.append(Message(user_id=sender,
                                    message_type=ATTACHMENT,
                                    message_data=generic_list_template(category_list, **{'provider': provider,
                                                                                         'type': 'get_category'}),
                                    quick_replies=quick_replies_instance))
        return messages

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

    def why_bot(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['happens', 'no_memory']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        return [Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Буває, що комусь хочете зробити приємність чи віддячити",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="проте людина далеко і у вас нема часу із нею зустрітись?😬",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="(або бажання😄)",
                        quick_replies=quick_replies_instance)]

    def happens(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['something_else', 'cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        return [Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Ну ось! А тепер можете з моєю допомогою купити щось смачне і надіслати тому, кого треба віддячити🙂",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="І людина сама забере ваш їстівний подарунок в зручний час і буде аж на сьомому небі від щастя😁",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Натисніть на «Заклади» і зробимо це прямо зараз😉",
                        quick_replies=quick_replies_instance)]

    def no_memory(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['yeah', 'half']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        return [Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Ну дивіться",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Буває так що у вашої половинки❤️ жахливий настрій☹️, а ви не поруч і не можете втішити чи допомогти?🤷‍",
                        quick_replies=quick_replies_instance)]

    def something_else(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['yeah', 'half']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        return [Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Ну дивіться",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Буває так що у вашої половинки❤️ жахливий настрій☹️, а ви не поруч і не можете втішити чи допомогти?🤷‍",
                        quick_replies=quick_replies_instance)]

    def yeah(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['something_hmm_else', 'cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        return [Message(user_id=sender,
                        message_type=TEXT,
                        message_data="То тепер ви знаєте, що завжди можете на відстані підняти настрій своїй половинці❤️",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Чи то надіславши морозиво🍦, чи то тірамісу🍮 із кавою",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Тисніть на «Заклади» і порадуєм вашу любов❤️ прямо зараз🙂",
                        quick_replies=quick_replies_instance)]

    def something_hmm_else(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['that_is_me', 'cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        return [Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Тільки чесно!",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Проспорили другові бургер🍔 і ніяк не віддасте, бо нема часу зустрітись?😅",
                        quick_replies=quick_replies_instance)]

    def half(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['that_is_me', 'not_really']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        return [Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Не зважайте😅",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Тоді ось що",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Тільки чесно!",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Проспорили другові бургер🍔 і ніяк не віддасте, бо нема часу зустрітись?😅",
                        quick_replies=quick_replies_instance)]

    def that_is_me(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        return [Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Ну то давайте прямо зараз оберемо якийсь смачнющий бургер🍔 і надішлемо йому!🙂",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="А він забере його коли буде час",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Натискайте «Заклади» та обирайте потрібний😉",
                        quick_replies=quick_replies_instance)]

    def not_really(self, sender, **kwargs) -> List[Message]:
        quick_replies_list = ['cafes']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               None)
        return [Message(user_id=sender,
                        message_type=TEXT,
                        message_data="А ви точно з цієї планети?😂",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Та я жартую)",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Ну то давайте придбаємо щось цікаве для вашого знайомого, в якого був нещодавно день народження, а ви забули привітати😅",
                        quick_replies=quick_replies_instance),
                Message(user_id=sender,
                        message_type=TEXT,
                        message_data="Нажміть на «Заклади» і обирайте щось смачне😋 і оригінальне😁",
                        quick_replies=quick_replies_instance)]

    @require_provider
    def add_product(self, sender, **kwargs) -> List[Message]:
        provider = kwargs.get('provider')
        adapter = self.adapters.get(provider)

        result = adapter.add_product(**kwargs)
        quick_replies_list = ['categories', 'payment', 'basket', 'why_bot']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=result,
                    quick_replies=quick_replies_instance),
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data=' Додайте щось іще або проведіть оплату💳, натиснувши клавішу "До оплати"',
                    quick_replies=quick_replies_instance)
        ]
        return messages

    @require_provider
    def remove_product(self, sender, **kwargs) -> List[Message]:
        provider = kwargs.get('provider')
        adapter = self.adapters.get(provider)

        result = adapter.remove_product(**kwargs)
        quick_replies_list = ['why_bot', 'categories', 'payment', 'basket']
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

        quick_replies_list = ['why_bot', 'categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        result = adapter.get_categories(**kwargs)
        rearranged_categories = transform(result)

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data="Щоб обрати категорію меню - натисніть на її назву.",
                    quick_replies=quick_replies_instance)
        ]
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

        quick_replies_list = ['why_bot', 'categories', 'payment', 'basket']
        quick_replies_instance = quick_replies(quick_replies_list,
                                               provider)

        result = adapter.get_products(**kwargs)
        if not result:
            return [Message(user_id=sender,
                            message_type=TEXT,
                            message_data="У цій категорії нема продуктів.",
                            quick_replies=quick_replies_instance)]

        rearranged_products = transform(result)

        messages = [
            Message(user_id=sender,
                    message_type=TEXT,
                    message_data='Щоб додати позицію до кошику 🛒  - натисніть клавішу "Додати"',
                    quick_replies=quick_replies_instance)
        ]
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
        quick_replies_list = ['why_bot', 'categories', 'payment', 'basket']
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
        quick_replies_list = ['why_bot', 'categories', 'payment', 'basket']
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

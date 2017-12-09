from .adapters.unit_adapter import UnitAdapter
from .fb_templates import *
from .utils import *


class Controller:
    adapters = {
        'Unit': UnitAdapter()
    }

    def check_valid_response(self, data):
        if not data:
            return False
        if 'delivery' in data:
            return False
        if 'read' in data:
            return False
        if 'is_echo' in data.get('message', {}):
            return False
        return True

    def get_message_payload(self, data):
        payload = None
        if data.get('message', {}).get('quick_reply'):
            payload = data.get('message', {}).get('quick_reply', {}).get('payload')
        elif 'postback' in data:
            payload = data.get('postback', {}).get('payload')
        return payload

    def get_sender(self, data):
        return data.get('sender').get('id')

    def make_body(self, reply_type, user_id, provider, items_to_show):
        data = []
        if reply_type in payloads.keys():
            payload = payloads.get(reply_type, {})
            payload.update({'provider': provider})

            button_type = button_types.get(reply_type)

            result = []
            items = transform(items_to_show)

            for item in items:
                if len(item) == 1:
                    result.append(generic_template(reply_type, item[0], button_type, **payload))
                else:
                    result.append((list_template(reply_type, button_type, *item, **payload)))

            data = [{
                "recipient": {"id": user_id},
                "message": {"attachment": item,
                            "quick_replies": quick_replies(reply_type, provider)}
            } for item in result]

        elif reply_type in text_types:
            try:
                text = text_types.get(reply_type).format(order_id=items_to_show.get('order_id', ''),
                                                         order_code=items_to_show.get('order_code', ''),
                                                         confirm_code=items_to_show.get('confirm_code', ''))
            except Exception:
                if isinstance(items_to_show, str):
                    text = items_to_show
                else:
                    text = text_types.get(reply_type)

            data = [{
                "recipient": {"id": user_id},
                "message": {"text": text,
                            "quick_replies": quick_replies(reply_type, provider)}
            }]
        elif reply_type in link_types:
            save_order_data(user_id, items_to_show)
            if reply_type == "checkout":
                if items_to_show.get('order_id') is not None:
                    url = link_types.get(reply_type) + '/order/' + str(items_to_show.get('order_id'))
                    data = [{
                        "recipient": {"id": user_id},
                        "message": {"attachment": generic_link_template(url, 'Пожалуйста, оплатите ваш заказ.'),
                                    "quick_replies": quick_replies(reply_type, provider)}
                    }]
                else:
                    data = [{
                        "recipient": {"id": user_id},
                        "message": {"text": "Сталася помилка, спробуйте ще.",
                                    "quick_replies": quick_replies(reply_type, provider)}}]
        else:
            print("TYPE", reply_type)
            print("ITEMS_TO_SHOW", items_to_show)
            data = [{
                "recipient": {"id": user_id},
                "message": {"attachment": receipt_template(**{'orders': items_to_show}),
                            "quick_replies": quick_replies(reply_type, provider)}
            }]
        return data

    def make_responses(self, **kwargs):
        responses = []
        data = kwargs.get('data')
        sender = self.get_sender(data)
        payload_data = self.get_message_payload(data)
        if not payload_data:
            payload_data = '{"type": "get_started","provider": "Unit"}'

        try:
            payload = json.loads(payload_data)
        except ValueError:
            payload = {'type': 'get_started',
                       'provider': 'Unit'}

        if isinstance(payload, str):
            payload = json.loads(payload)
        provider = payload.get('provider')

        adapter = self.adapters.get(provider)
        reply_type = payload.get('type')
        orders = get_orders(sender) or []

        if reply_type == 'checkout':

            if not orders:
                responses = self.make_body('no_products',
                                           sender,
                                           payload.get('provider'),
                                           orders)
            else:
                data = adapter.checkout(**{'orders': orders})
                responses.extend(self.make_body('checkout',
                                                sender,
                                                payload.get('provider'),
                                                data))
        elif reply_type in adapter.methods.keys():
            id_type = id_types.get(reply_type, {}).get('self_id')
            items_to_show = adapter.methods.get(reply_type)(
                **{
                    id_type: payload.get(id_type),
                    'user_id': sender,
                    'provider': provider,
                    'mongo': mongo,
                    'orders': orders
                }
            )
            responses = self.make_body(payload.get('type'),
                                       sender,
                                       payload.get('provider'),
                                       items_to_show)
        else:
            items_to_show = get_orders(sender) or []
            if not items_to_show and payload.get('type') == 'get_basket':
                responses = self.make_body('no_products',
                                           sender,
                                           payload.get('provider'),
                                           items_to_show)
            else:
                responses = self.make_body(payload.get('type'),
                                           sender,
                                           payload.get('provider'),
                                           items_to_show)
        return responses

def transform(items):
    result, temp = [], []
    div = 10
    for item in items:
        temp.append(item)
        if len(temp) == div:
            result.append(temp)
            temp = []
    if len(temp) <= 1 and result:
        result[-1].extend(temp)
    else:
        result.append(temp)
    return result


def get_or_create_order(document, user_id, provider):
    instance = document.find_one({'user_id': user_id,
                                  'provider': provider})
    if not instance:
        instance = document(**{'user_id': user_id,
                               'provider': provider})
        instance.commit()
    return instance


def require_provider(func):
    def wrapped(self, sender, **kwargs):
        provider = kwargs.get('provider')
        if not provider:
            return []
        return func(self, sender, **kwargs)
    return wrapped


def rework_checkout_data(data, **kwargs):
    data.update({'cook_time': str(data.get('cook_time')),
                 'order_id': str(data.get('order_id'))})
    data.update(kwargs)
    return data
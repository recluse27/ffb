from . import app

FB_REQUEST_URL = "https://graph.facebook.com/v2.9/me/messages?access_token=" \
                 + app.config['PAGE_ACCESS_TOKEN']

HEADERS = {'Content-Type': 'application/json',
           'user-agent': 'Mozilla/5.0 (Macintosh; '
                         'Intel Mac OS X 10_13_0) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/61.0.3163.100 Safari/537.36'}
UNIT_REPLY_EXPLAIN = lambda **kwargs: ("Ви щойно зробили покупку за допомогою Friendly Food Bot🙂. "
                                       "Код замовлення - {order_code}, "
                                       "код підтвердження - {confirm_code}. "
                                       "Перешліть наступне повідомлення Вашому другу, якого хочете почастувати, "
                                       "і він зможе отримати подарунок🎁 в "
                                       "будь-який зручний для нього час протягом 14 днів з {date}. "
                                       "Friendly Food Bot із задоволенням допоможе Вам ще😉! Всього найкращого!🙂").format(
    order_code=kwargs.get('order_code'),
    confirm_code=kwargs.get('confirm_code'),
    date=kwargs.get('date')
)

UNIT_REPLY_GIFT = lambda **kwargs: ("Якщо Ви читаєте це повідомлення - значить його відправник вирішив "
                                    "пригостити Вас чимось смачненьким в UNIT Cafe (вул. Дорогожицька, 1) "
                                    "за допомогою Friendly Food bot😋. \n"
                                    "https://www.facebook.com/FriendlyFoodBot/ \n"
                                    "Ви можете прийти в будь-який зручний для Вас час "
                                    "з 9:30 до 21:00 протягом наступних 14 днів з {date} "
                                    "і отримати свій їстівний подарунок🎁. "
                                    "Для цього Вам потрібно лише показати касиру або офіціантові наступну інформацію: \n"
                                    "Код замовлення - {order_code}, "
                                    "код підтвердження - {confirm_code}. "
                                    "Пам’ятайте, Friendly food bot завжди з радістю "
                                    "допоможе Вам пригостити Ваших друзів. Смачного!😉").format(
    order_code=kwargs.get('order_code'),
    confirm_code=kwargs.get('confirm_code'),
    date=kwargs.get('date')
)

UNIT_REPLY_TEXT = lambda **kwargs: ("Вы только что совершили покупку с помощью Friendly Food Bot. "
                                    "Код заказа - {order_code}, "
                                    "код подтверждения - {confirm_code}. "
                                    "Перешлите предыдущее сообщение вашему другу, которого хотите угостить, "
                                    "и он сможет получить подарок в любое удобное для него время. "
                                    "Friendly Food Bot с удовольствием поможет вам ещё. "
                                    "Для этого нужно написать и отправить любое текстовое сообщение "
                                    "в чат с Friendly Food Bot. Ждём вас снова! Всего наилучшего!").format(
    order_code=kwargs.get('order_code'),
    confirm_code=kwargs.get('confirm_code')
)

GREETING = ("Привіт🙂! Вітаємо у Friendly food bot! "
            "За допомогою нашого сервісу  ви зможете почастувати друзів і "
            "знайомих різними смаколиками🥤🍩🍰 з UNIT Cafe, а з часом і з інших закладів🙂. "
            "Слідуйте вказівкам бота та дивуйте друзів неочікуваними смачними подарунками!😉")

CACHE_UPDATE_DAYS = 1

UNIT_PUB_KEY = "i93305383988"

UNIT_PRIV_KEY = "NigKQ1DBXNaQUuHh8sG7yaU3bleRWApuaakbIfwm"

SELF_URL = "http://friendlybot.westeurope.cloudapp.azure.com"

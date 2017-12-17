from . import app

FB_REQUEST_URL = "https://graph.facebook.com/v2.9/me/messages?access_token=" \
                 + app.config['PAGE_ACCESS_TOKEN']

HEADERS = {'Content-Type': 'application/json',
           'user-agent': 'Mozilla/5.0 (Macintosh; '
                         'Intel Mac OS X 10_13_0) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/61.0.3163.100 Safari/537.36'}
UNIT_REPLY_EXPLAIN = ("Ви тільки що зробили покупку за допомогою Friendly Food Bot🙂. "
                      "ID замовлення - {order_id}, "
                      "код замовлення - {order_code}, "
                      "код підтвердження - {confirm_code}. "
                      "Перешліть наступне повідомлення вашому другу, якого хочете почастувати, "
                      "і він зможе отримати подарунок🎁 в будь-який зручний для нього час. "
                      "Friendly Food Bot із задоволенням допоможе вам ще😉! Всього найкращого!🙂")

UNIT_REPLY_GIFT = ("Якщо ви читаєте це повідомлення - значить його відправник вирішив "
                   "пригостити вас чимось смачненьким в UNIT Cafe (вул. Дорогожицька, 1) "
                   "за допомогою Friendly Food bot😋. \n"
                   "https://www.facebook.com/FriendlyFoodBot/ \n"
                   "Ви можете прийти в будь-який зручний для вас час "
                   "з 9:00 до 21:00 і отримати свій їстівний подарунок🎁. "
                   "Для цього вам потрібно лише показати касиру або офіціантові наступну інформацію: \n"
                   "ID замовлення - {order_id}, "
                   "код замовлення - {order_code}, "
                   "код підтвердження - {confirm_code}. "
                   "Пам’ятайте, Friendly food bot завжди із радістю "
                   "допоможе вам пригостити ваших друзів. Смачного!😉")


UNIT_REPLY_TEXT = ("Вы только что совершили покупку с помощью Friendly Food Bot. "
                   "ID заказа - {order_id}, код заказа - {order_code}, "
                   "код подтверждения - {confirm_code}. "
                   "Перешлите предыдущее сообщение вашему другу, которого хотите угостить, "
                   "и он сможет получить подарок в любое удобное для него время. "
                   "Friendly Food Bot с удовольствием поможет вам ещё. "
                   "Для этого нужно написать и отправить любое текстовое сообщение "
                   "в чат с Friendly Food Bot. Ждём вас снова! Всего наилучшего!")


GREETING = ("Привіт🙂! Вітаємо у Friendly food bot! "
            "За допомогою нашого сервісу  ви зможете почастувати друзів і "
            "знайомих різними смаколиками🥤🍩🍰 з UNIT Cafe, а з часом і з інших закладів🙂. "
            "Слідуйте вказівкам бота та дивуйте друзів неочікуваними смачними подарунками!😉")


CACHE_UPDATE_DAYS = 1

UNIT_PUB_KEY = "i93305383988"

UNIT_PRIV_KEY = "NigKQ1DBXNaQUuHh8sG7yaU3bleRWApuaakbIfwm"

SELF_URL = "http://friendlybot.westeurope.cloudapp.azure.com"

from . import app

FB_REQUEST_URL = "https://graph.facebook.com/v2.9/me/messages?access_token=" \
                 + app.config['PAGE_ACCESS_TOKEN']

HEADERS = {'Content-Type': 'application/json',
           'user-agent': 'Mozilla/5.0 (Macintosh; '
                         'Intel Mac OS X 10_13_0) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/61.0.3163.100 Safari/537.36'}
UNIT_REPLY_TEXT = "Вы только что совершили покупку с помощью Friendly Food Bot. "
"ID заказа - {order_id}, код заказа - {order_code}, код подтверждения - {confirm_code}. "
"Перешлите предыдущее сообщение вашему другу, которого хотите угостить, "
"и он сможет получить подарок в любое удобное для него время. "
"Friendly Food Bot с удовольствием поможет вам ещё. Для этого "
"нужно написать и отправить любое текстовое сообщение в чат с Friendly Food Bot. "
"Ждём вас снова! Всего наилучшего!"

from FoodBot import testing, app

HEADERS = {'Content-Type': 'application/json',
           'user-agent': 'Mozilla/5.0 (Macintosh; '
                         'Intel Mac OS X 10_13_0) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/61.0.3163.100 Safari/537.36'}

REPLY_EXPLAIN = lambda **kwargs: ("Ви щойно зробили покупку за допомогою Friendly Food Bot🙂. "
                                  "Код замовлення - {order_code}, "
                                  "код підтвердження - {confirm_code}. "
                                  "Перешліть наступне повідомлення Вашому другу, якого хочете почастувати, "
                                  "і він зможе отримати подарунок🎁 в "
                                  "будь-який зручний для нього час до {date}. "
                                  "Friendly Food Bot із задоволенням допоможе Вам ще😉! Всього найкращого!🙂").format(
    order_code=kwargs.get('order_code'),
    confirm_code=kwargs.get('confirm_code'),
    date=kwargs.get('date')
)

REPLY_GIFT = lambda **kwargs: ("Якщо Ви читаєте це повідомлення - значить його відправник вирішив "
                               "пригостити Вас чимось смачненьким в {cafe_name} "
                               "за допомогою Friendly Food bot😋. \n"
                               "http://m.me/FriendlyFoodBot \n"
                               "Ви можете прийти в будь-який зручний для Вас час "
                               "з 9:30 до 21:00 до {date} "
                               "і отримати свій їстівний подарунок🎁 у будь-якому закладі {cafe_name}. "
                               "Для цього Вам потрібно лише показати касиру або офіціантові наступну інформацію: \n"
                               "Код замовлення - {order_code}, "
                               "код підтвердження - {confirm_code}. "
                               "Пам’ятайте, Friendly food bot завжди з радістю "
                               "допоможе Вам пригостити Ваших друзів. Смачного!😉").format(
    order_code=kwargs.get('order_code'),
    confirm_code=kwargs.get('confirm_code'),
    cafe_name=kwargs.get('cafe_name'),
    date=kwargs.get('date')
)

REPLY_TEXT = lambda **kwargs: ("Вы только что совершили покупку с помощью Friendly Food Bot. "
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

TEXT = 'text'
ATTACHMENT = 'attachment'

GREETING = [
    "Привіт🙂!",
    "Я Friendly Food Bot!",
    "Я допоможу Вам пригостити друзів смаколиками🍰 на відстані, якщо немає можливості зустрітись із ними.🤷‍",
    "А друзі зможуть отримати його у будь-який зручний час у тому закладі чи мережі, де Ви придбали подарунок!🙂",
    "Натисніть «Заклади» та оберіть той, в якому бажаєте придбати подарунок!🎁",
]

INSTRUCTION = {
    "initial": [
        "Як я вже казав - я можу допомогти Вам зробити смачний подарунок 🥤Вашим друзям з різних кафе, який вони зможуть скуштувати у будь-який зручний для них час⏳"],
    "how_to_buy": ["1. Натисніть «Заклади» і оберіть той, у якому Ви бажаєте придбати подарунок🎁.",
                   "2. Оберіть необхідну категорію меню.",
                   "3. Натисніть на клавішу «Додати», під необхідною позицією обраної категорії.",
                   "4. Натисніть на клавішу «Кошик»🛒 і перегляньте його вміст. Це не є обов’язковим, проте я раджу завжди перевіряти кошик.",
                   "Після того як кошик наповнено різними смаколиками🥤🍰🍩і його вміст перевірено - треба провести оплату.💳",
                   "До речі, я не беру комісії за свої послуги😉"],
    "how_to_pay": ["Дуже просто🙂!",
                   "Натисніть клавішу «До оплати» та у повідомленні, що з‘явилося у новому вікні, натисніть «Перейти до оплати».",
                   "Вас буде перенаправлено до системи електронних платежів LiqPay, де требе буде оплатити подарунок за допомогою банківської картки💳.",
                   "Після успішної оплати закрийте вікно з LiqPay, так як підтвердження оплати я надішлю Вам у цей чат. Тепер Ви можете подарувати смаколик, котрий придбали!🎁"],
    "how_to_present": ["Після оплати я надішлю Вам три повідомлення:",
                       "Перше - підтвердження Вашої операції і пояснення того, як подарувати придбаний смаколик, якщо раптом забудете🤷‍️",
                       "Друге - повідомлення, яке треба переслати Вашому другові, котрого Ви хочете пригостити. В цьому повідомленні буде міститись код замовлення і код підтвердження, які необхідно буде показати у закладі для отримання подарунку🎁.",
                       "Третє - чек.",
                       "Як бачите - усе просто!"],
    "how_details": ["Є дещо, на що я хочу звернути Вашу увагу☝️:",
                    "1. Ваш подарунок має бути використаний протягом 30 днів (14 днів у UNIT cafe) з моменту придбання. Про це я буду нагадувати у повідомленнях, котрі надішлю після оплати.",
                    "2. Замовлення не можна розбивати на декілька подарунків. Тобто, якщо Ви придбали за одну транзакцію декілька позицій з меню - це буде вважатися одним замовленням.",
                    "3. Ми не робимо доставку. Той, кому Ви зробили подарунок має самостійно отримати його у зручний для нього час у закладі, де подарунок було придбано.",
                    "4. Ми не можемо гарантувати🤷‍️, що подарунок буде видано його утримувачу в будь-який час будь-якого дня. Заклади можуть в деякий період не мати потрібного товару, тому придеться прийти іншого разу.",
                    'Ось і усе! А тепер натисніть "Заклади" та зробіть подарунок!🙂']
}

WHY_BOT = ("Вам зробили невеличку послугу і Ви б ходіли подякувати людині, "
           "проте не знаєте як, бо Ви не поруч🤔? А може Ваша друга половинка знаходиться "
           "у іншому кінці міста у жахливому настрої😤 і Ви ніяк не можете їй допомогти або втішити? "
           "Чи може Ви проспорили другові бургер🍔, але немає можливості із ним зустрітись? "
           "Або Ваша дитина забула😰 вдома гроші на обід? Та й, в кінці кінців, "
           "може Вам просто хочеться зробити комусь приємність та підняти настрій😁, але Ви далеко?\n\n"
           "Зробіть це із Friendly food bot!🙂😉 Станьте ближче до людей, що Вам небайдужі🍩🍹☕️")

CACHE_UPDATE_DAYS = 1

UNIT_PUB_KEY = "i93305383988"

UNIT_PRIV_KEY = "NigKQ1DBXNaQUuHh8sG7yaU3bleRWApuaakbIfwm"

SELF_URL = "http://friendlybot.westeurope.cloudapp.azure.com"

BOT_URL = "https://graph.facebook.com/v2.9/me/messages?access_token=" + app.config['PAGE_ACCESS_TOKEN'
if not testing else "PAGE_TEST_TOKEN"]

CAFE_SYSTEM_URL = "http://cafesystem.herokuapp.com/" if not testing else "http://cafetestsystem.herokuapp.com/"

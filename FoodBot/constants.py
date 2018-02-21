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
                                  "будь-який зручний для нього час протягом 14 днів з {date}. "
                                  "Friendly Food Bot із задоволенням допоможе Вам ще😉! Всього найкращого!🙂").format(
    order_code=kwargs.get('order_code'),
    confirm_code=kwargs.get('confirm_code'),
    date=kwargs.get('date')
)

REPLY_GIFT = lambda **kwargs: ("Якщо Ви читаєте це повідомлення - значить його відправник вирішив "
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

GREETING = ("Привіт🙂! Вітаємо у Friendly food bot! "
            "За допомогою нашого сервісу  ви зможете почастувати друзів і "
            "знайомих різними смаколиками🥤🍩🍰 з UNIT Cafe, а з часом і з інших закладів🙂. "
            "Слідуйте вказівкам бота та дивуйте друзів неочікуваними смачними подарунками!😉")

INSTRUCTION = ("Friendly food bot - це Facebook messenger бот, з допомогою якого"
               " Ви маєте можливість дарувати їстівні подарунки 🍩🥤🍦своїм друзям"
               " та знайомим з різних кафе та мереж харчування🙂 (наразі бот працює"
               " тільки у UNIT cafe, вул. Дорогожицька 1).\nОтже, для того, щоб пригостити"
               " друга Вам необхідно:\n1) Обрати позицію у меню, котра Вас цікавить. "
               "Для цього натисніть клавішу «Категорії» та оберіть із категорій, що з’явилися,"
               " необхідну.\n2) Натиснути клавішу «Додати» навпроти необхідної позиції.\n3) Перевірити кошик. "
               "Для цього натисніть клавішу «Кошик» і перегляньте, чи відповідає вміст кошика тому,"
               " що Ви бажаєте придбати. Це не є обов’язковим, проте ми радимо перевіряти кошик "
               "задля того, щоб переконатися, що Ви додали саме те, що хотіли😉.\nВи завжди "
               "можете видалити із кошика ту чи іншу позицію, натиснувши клавішу «Видалити» "
               "навпроти необхідної позиції.\n4) Провести оплату. Натисніть клавішу «До оплати» "
               "та у повідомленні, що з‘явилося, натисніть «Перейти до оплати». Вас буде "
               "перенаправлено до системи електронних платежів LiqPay, де Вам буде "
               "запропоновано оплатити подарунок за допомогою електронної картки.\n5) "
               "Зробити подарунок🎁! Після того, як Ви проведете оплату - бот надішле Вам "
               "три повідомлення. Перше - підтвердження Вашої операції і пояснення того, як "
               "подарувати придбаний смаколик🙂. Друге - повідомлення, яке треба переслати "
               "Вашому другові, котрого Ви хочете пригостити😉. В цьому повідомленні буде міститись "
               "код замовлення і код підтвердження, які необхідно буде показати у закладі для "
               "отримання подарунку😋. Третє - чек.\n\nЗверніть увагу:\n- Ваш подарунок має "
               "бути використаний протягом 14 днів з моменту придбання. Про це буде написано "
               "у повідомленнях, котрі Ви отримаєте після оплати.\n- Замовлення не можна розбивати "
               "на декілька подарунків. Тобто, якщо Ви придбали за одну транзакцію декілька "
               "позицій з меню - це буде вважатися одним замовленням. Тому, якщо Ви хочете "
               "пригостити декількох людей\n- Вам треба пройти пункти 1-5 стільки разів, "
               "скількох друзів Ви бажаєте пригостити.")

CACHE_UPDATE_DAYS = 1

UNIT_PUB_KEY = "i93305383988"

UNIT_PRIV_KEY = "NigKQ1DBXNaQUuHh8sG7yaU3bleRWApuaakbIfwm"

SELF_URL = "http://friendlybot.westeurope.cloudapp.azure.com"

BOT_URL = "https://graph.facebook.com/v2.9/me/messages?access_token=" + app.config['PAGE_ACCESS_TOKEN'
if not testing else "PAGE_TEST_TOKEN"]

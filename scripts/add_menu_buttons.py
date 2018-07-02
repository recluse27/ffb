import requests as rq

from config import PAGE_ACCESS_TOKEN, PAGE_TEST_TOKEN

url = "https://graph.facebook.com/v2.10/me/messenger_profile?access_token={token}"


def make_get_started(access_token):
    get_started = {
        "get_started": {"payload": "{\"type\":\"greeting\"}"}
    }

    res = rq.post(url=url.format(token=access_token), json=get_started)
    print(res)
    print(res.text)


def make_menu_buttons(access_token):
    data = {"persistent_menu":
        [
            {"locale": "default",
             "composer_input_disabled": True,
             "call_to_actions": [
                 {
                     "title": "Заклади",
                     "type": "postback",
                     "payload": "{\"type\":\"get_cafes\"}"
                 },
                 {
                     "title": 'Нащо мені це?',
                     "type": "postback",
                     "payload": "{\"type\":\"why_bot\"}"
                 },
                 {
                     "type": "postback",
                     "title": "Інструкція",
                     "payload": "{\"type\":\"get_instruction\"}"
                 }
             ]
             }
        ]
    }

    res = rq.post(url=url.format(token=access_token), json=data)
    print(res)
    print(res.text)


def make_actual_buttons():
    make_menu_buttons(PAGE_ACCESS_TOKEN)


def make_test_buttons():
    make_menu_buttons(PAGE_TEST_TOKEN)

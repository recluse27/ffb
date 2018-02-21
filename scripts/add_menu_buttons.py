import requests as rq

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
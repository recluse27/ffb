import json

import requests as rq


def make_buttons(access_token):
    url = "https://graph.facebook.com/v2.10/me/messenger_profile?access_token={token}".format(token=access_token)
    get_started = {
        "get_started": {"payload": "{\"type\":\"greeting\"}"}
    }

    res = rq.post(url=url, json=get_started)
    print(res)
    print(res.text)

    data = {"persistent_menu":
        [
            {"locale": "default",
             "call_to_actions": [
                 {
                     "title": "Категорії",
                     "type": "postback",
                     "payload": "{\"type\":\"get_categories\", \"provider\":\"unit\"}"
                 },
                 {
                     "type": "postback",
                     "title": "Інструкція",
                     "payload": "{\"type\":\"get_instruction\", \"provider\":\"unit\"}"
                 }
             ]
             }
        ]
    }

    res = rq.post(url=url, json=data)
    print(res)
    print(res.text)

import time

import requests as rq

ping_urls = ["https://foodappbot.herokuapp.com",
             "https://cafesystem.herokuapp.com/bot",
             "https://cafefront.herokuapp.com"]


def ping(minutes):
    while True:
        for ping_url in ping_urls:
            res = rq.get(url=ping_url)
            print(res)
        time.sleep(minutes * 60)


if __name__ == '__main__':
    ping(10)

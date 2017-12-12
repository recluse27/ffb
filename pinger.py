import time

import requests as rq

ping_url = "https://foodappbot.herokuapp.com"


def ping(minutes):
    while True:
        res = rq.get(url=ping_url)
        print(res)
        time.sleep(minutes * 60)


if __name__ == '__main__':
    ping(10)

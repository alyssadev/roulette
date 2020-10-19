#!/usr/bin/env python3
import requests
import flask
from json import load, dumps
from random import choice
from time import time
from os import environ

app = flask.Flask(__name__)
last_refresh = None
data = []

def refresh_data():
    global last_refresh
    global data
    if not last_refresh or time() - last_refresh > 120:
        data = requests.post("https://gql.twitch.tv/gql", headers={
                'Connection': 'keep-alive',
                'Authorization': 'OAuth ' + environ["TWITCH_OAUTH_SECRET"],
                'Accept-Language': 'en-US',
                'Client-Id': environ["TWITCH_OAUTH_ID"],
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43',
                'X-Device-Id': "".join(choice("abcdef0123456789") for _ in range(16)),
                'Content-Type': 'text/plain;charset=UTF-8',
                'Accept': '*/*',
                'Origin': 'https://www.twitch.tv',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://www.twitch.tv/'
            }, json=[ {
                "operationName":"BrowsePage_Popular",
                "variables": {
                    "limit":100,
                    "platformType":"all",
                    "options":{
                        "includeRestricted":["SUB_ONLY_LIVE"],
                        "sort":"VIEWER_COUNT_ASC",
                        "tags":[],
                        "recommendationsContext":{
                            "platform":"web"
                            }
                    },
                    "sortTypeIsRecency":False
                },
                "extensions":{
                    "persistedQuery":{
                        "version":1,
                        "sha256Hash":"c3322a9df3121f437182beb5a75c2a8db9a1e27fa57701ffcae70e681f502557"
                    }
                }
            } ]).json()
        print(dumps(data, indent=4))
        last_refresh = time()
    return data


@app.route('/')
def index():
    data = refresh_data()
    r = choice([
        e["node"]["broadcaster"]["login"] for e in data[0]["data"]["streams"]["edges"]
          if e["node"]["viewersCount"] < 5
    ])
    return flask.redirect("https://twitch.tv/{}".format(r))

if __name__ == "__main__":
    app.run(host="0.0.0.0")

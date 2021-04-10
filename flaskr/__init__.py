from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import requests
import json

app = Flask(__name__)

# 環境変数からアクセストークンとChannel Secretをを取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# class CoinZApi:
#     def __init__(self):
#         self.endpoint = 'https://api.coin.z.com/public'
#         self.path = '/v1/ticker'
#         self.symbol = ''
#
#     def set_symbol(self, symbol):
#         self.symbol = symbol

endpoint = 'https://api.coin.z.com/public'
path = '/v1/ticker'
symbol = 'BTC'


def make_symbol_path(symbol):
    return path + '?symbol=' + symbol


@app.route('/')
def index():
    return 'second Page'


@app.route('/btc')
def re_json():
    symbol_patth = make_symbol_path(symbol)
    res = requests.get(endpoint + symbol_patth)
    ask = json.loads(res.text)["data"][0]["ask"]
    bid = json.loads(res.text)["data"][0]["bid"]
    return '買値' + str(ask) + ' ' + '売値' + str(bid)

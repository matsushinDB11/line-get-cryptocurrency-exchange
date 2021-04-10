from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent
import os
import requests
import json

app = Flask(__name__)

# 環境変数からアクセストークンとChannel Secretをを取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

endpoint = 'https://api.coin.z.com/public'
path = '/v1/ticker'
symbol = 'BTC'


def make_symbol_path(symbol):
    return path + '?symbol=' + symbol


@app.route('/')
def index():
    return 'line-get-cryptocurrency-exchange by Matsushin'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='初めまして 登録ありがとう')
    )


@handler.add(MessageEvent, message=TextMessage)
def re_btc(event):
    symbol_path = make_symbol_path(symbol)
    res = requests.get(endpoint + symbol_path)
    ask = json.loads(res.text)["data"][0]["ask"]
    bid = json.loads(res.text)["data"][0]["bid"]
    msg = '買値' + str(ask) + ' ' + '売値' + str(bid)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg)
    )


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


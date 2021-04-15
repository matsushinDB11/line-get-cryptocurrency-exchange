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
# symbol = 'BTC'


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


def get_symbol_list(msg):
    """メッセージに含まれるシンボルをリストで返す
    引数 msg: 文字列型
    戻り値 文字列 リスト"""
    symbol_list = []
    if 'BTC' in msg:
        symbol_list.append('BTC')
    if 'ETH' in msg:
        symbol_list.append('ETH')
    if 'BCH' in msg:
        symbol_list.append('BCH')
    if 'LTC' in msg:
        symbol_list.append('LTC')
    if 'XRP' in msg:
        symbol_list.append('XRP')
    return symbol_list


@handler.add(MessageEvent, message=TextMessage)
def re_btc(event):
    symbol_list = get_symbol_list(event.message.text)
    re_msg = ''
    if not symbol_list:
        re_msg += 'メッセージに有効なシンボルが含まれていません'
    else:
        for symbol in symbol_list:
            symbol_path = make_symbol_path(symbol)
            res = requests.get(endpoint + symbol_path)
            ask = json.loads(res.text)["data"][0]["ask"]
            bid = json.loads(res.text)["data"][0]["bid"]
            msg = '現在' + symbol + 'のレートは\n' + 'ASK: ' + str(ask) + '\n' + 'BID: ' + str(bid) + '\n'
            re_msg += msg
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=re_msg)
    )


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


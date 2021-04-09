from flask import Flask
import requests
import json

app = Flask(__name__)

endpoint = 'https://api.coin.z.com/public'
path = '/v1/ticker'
symbol = 'BTC'


def make_symbol_path(symbol):
  return path + '?symbol=' + symbol


@app.route('/')
def index():
  return 'first Page'


@app.route('/btc')
def re_json():
  symbol_patth = make_symbol_path(symbol)
  res = requests.get(endpoint + symbol_patth)
  ask = json.loads(res.text)["data"][0]["ask"]
  bid = json.loads(res.text)["data"][0]["bid"]
  return '買値' + str(ask) + ' ' + '売値' + str(bid)


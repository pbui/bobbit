# stock.py

from urllib.parse import urlencode

import json
import os
import yaml

import tornado.gen
import tornado.httpclient

# Metadata

NAME    = 'stock'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!stock (?P<symbol>.*$)'
USAGE   = '''Usage: !stock <symbol>
Given a stock symbol, this returns the daily stock pricing information.
Example:
    > !stock TSLA
    Symbol: TSLA, Price: 815.56, Open: 820.5, High: 826, Low: 811.8, Change: 4.94
'''

# Constants

API_URL = 'https://finnhub.io/api/v1/quote'
API_KEY = None

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, symbol=None):
    params = {'symbol': symbol.upper(), 'token': API_KEY}
    url    = API_URL + '?' + urlencode(params)
    client = tornado.httpclient.AsyncHTTPClient()
    result = yield tornado.gen.Task(client.fetch, url)
    try:
        data     = json.loads(result.body.decode())
        response = bot.format_text(
            "{bold}Symbol{bold}: {symbol}, "
            "{bold}Price{bold}: {price}, "
            "{color}{cyan}Open{color}: {price_open}, "
            "{color}{green}High{color}: {day_high}, "
            "{color}{red}Low{color}: {day_low}, "
            "{color}{yellow}Change{color}: {day_change:0.2f}",
            symbol     = symbol.upper(),
            price      = data['c'],
            price_open = data['o'],
            day_high   = data['h'],
            day_low    = data['l'],
            day_change = data['o'] - data['c'],
        )
    except (KeyError, json.decoder.JSONDecodeError) as e:
        bot.logger.exception(e)
        response = 'No results'

    bot.send_response(response, nick, channel)

# Register

def register(bot):
    global API_KEY

    config_path = os.path.join(bot.config_dir, 'stocks.yaml')
    try:
        config  = yaml.safe_load(open(config_path))
        API_KEY = config.get('api_key', '')
    except (IOError, KeyError) as e:
        bot.log.warn(e)

    if not API_KEY:
        return []

    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

# taunts.py

import datetime
import json
import re

import tornado.gen
import tornado.httpclient

# Metadata

NAME    = 'aoe2calendar'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!aoe2calendar\s*(?P<today>\d{2}/\d{2}/\d{4})*'
USAGE   = '''Usage: !aoe2calendar [M/D/Y]
List all Age of Empires II events from aoe2calendar.com based on provided date
(default is today).

Example:
    > !aoe2calendar
    ...
'''

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, today=None):
    today    = today or datetime.date.today().strftime('%m/%d/%Y')
    client   = tornado.httpclient.AsyncHTTPClient()
    result   = yield tornado.gen.Task(client.fetch, 'https://aoe2calendar.com/')
    text     = re.findall(r'"matches":(\[.*\]),"flags"', result.body.decode())
    matches  = json.loads(text[0])
    matches  = filter(lambda m: m['time'] >= today, matches)
    response = ['{}: {} - {} - {}'.format(m['time'], m['title'], m['round'], m['format']) for m in matches]
    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

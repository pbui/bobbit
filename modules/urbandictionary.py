# urbandictionary.py

from urllib.parse import urlencode

import json

import tornado.gen
import tornado.httpclient

# Metadata

NAME    = 'urbandictionary'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!ud (?P<query>.*$)'
USAGE   = '''Usage: !ud <query>
Given a search query, this returns the first result from Urban Dictionary
Example:
    > !ud pancakes
'''

# Constants

UD_URL      = 'http://api.urbandictionary.com/v0/define'
UD_TEMPLATE = '{color}{green}{word}{color} is {bold}{definition}{bold}; an example is: {color}{cyan}{example}{color} @ {color}{blue}{url}{color}'

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, query=None):
    params = {'term': query}
    url    = UD_URL + '?' + urlencode(params)
    client = tornado.httpclient.AsyncHTTPClient()
    result = yield tornado.gen.Task(client.fetch, url)

    try:
        data     = json.loads(result.body.decode())['list'][0]
        response = bot.format_text(UD_TEMPLATE,
            word       = data['word'],
            definition = data['definition'].strip().replace('\r', ' ').replace('\n', ' '),
            example    = data['example'].strip().replace('\r', ' ').replace('\n', ' '),
            url        = data['permalink'],
        )
    except (IndexError, ValueError) as e:
        bot.logger.warn(e)
        response = 'No results'

    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

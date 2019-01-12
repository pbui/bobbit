# weather.py

'''
Configuration
=============

The weather module reads from the weather.yaml file stored in bobbit's working
directory and expects the following values:

    appid:      This is the Open Weather Map APPID
    default:    This is the default zip code

'''

from urllib.parse import urlencode

import json
import os
import yaml

import tornado.gen
import tornado.httpclient

# Metadata

NAME    = 'weather'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!weather\s*(?P<zipcode>\d{5})*$'
USAGE   = '''Usage: !weather <zip code>
Given a zip code, this returns the current weather for that location
Example:
    > !weather          # Default location
    > !weather 46556    # Specific zip code
'''

# Constants

OWM_URL   = 'http://api.openweathermap.org/data/2.5/weather'
OWM_APPID = None
ZIPCODE   = {
    '#nd-cse':  46556, # Notre Dame, IN
    '#ndlug':   46556, # Notre Dame, IN
    '#uwec-cs': 54702, # Eau Claire, WI
}
DEFAULT_ZIPCODE = None

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, zipcode=None):
    zipcode = zipcode or ZIPCODE.get(channel, DEFAULT_ZIPCODE)
    params  = {
        'zip':   zipcode,
        'appid': OWM_APPID,
        'units': 'imperial',
    }
    url    = OWM_URL + '?' + urlencode(params)
    client = tornado.httpclient.AsyncHTTPClient()
    result = yield tornado.gen.Task(client.fetch, url)

    try:
        data     = json.loads(result.body.decode('utf-8'))
        temp     = data['main']['temp']
        text     = data['weather'][0]['description']
        response = 'Current weather is {}°F, {}'.format(temp, text.title())
    except (KeyError, IndexError, ValueError):
        response = 'No results'

    bot.send_response(response, nick, channel)

# Register

def register(bot):
    global OWM_APPID, DEFAULT_ZIPCODE

    config          = yaml.load(open(os.path.join(bot.config_dir, 'weather.yaml')))
    DEFAULT_ZIPCODE = config.get('default', ZIPCODE['#ndlug'])
    OWM_APPID       = config.get('appid', None)

    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

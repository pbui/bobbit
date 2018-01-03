# weather.py -------------------------------------------------------------------

from urllib.parse import urlencode

import json
import tornado.gen
import tornado.httpclient

# Meta-data --------------------------------------------------------------------

NAME    = 'weather'
ENABLE  = True
TYPE    = 'command'
PATTERN0= '^!weather$'
PATTERN1= '^!weather (?P<zipcode>\d{5})'
USAGE   = '''Usage:  !weather <zip code>
Given a zip code, this returns the current weather for that location
Example:
    > !weather          # Default location
    > !weather 46556    # Specific zip code
'''

# Constants --------------------------------------------------------------------

OWM_URL = 'http://api.openweathermap.org/data/2.5/weather'

ZIPCODE = { 
    '#nd-cse':  46556, # Notre Dame, IN
    '#ndlug':   46556, # Notre Dame, IN
    '#uwec-cs': 54702, # Eau Claire, WI
}

# Command ----------------------------------------------------------------------

def command(bot, nick, message, channel, zipcode=None):
    default = bot.config.get('weather', {}).get('zipcode', ZIPCODE['#ndlug'])
    zipcode = ZIPCODE.get(channel, zipcode or default)
    params  = {
        'zip':   zipcode,
        'APPID': bot.config.get('weather', {}).get('appid', None),
        'units': 'imperial',
    }
    url     = OWM_URL + '?' + urlencode(params)
    result  = tornado.httpclient.HTTPClient().fetch(url)
    try:
        data     = json.loads(result.body.decode('utf-8'))
        temp     = data['main']['temp']
        text     = data['weather'][0]['description']
        response = 'Current weather is {}°F, {}'.format(temp, text.title())
    except (KeyError, IndexError, ValueError):
        response = 'No results'

    return bot.format_responses(response, nick, channel)

# Register ---------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN0, command),
        (PATTERN1, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------

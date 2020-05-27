# google.py

import html
import logging

from bobbit.utils import shorten_url

# Metadata

NAME    = 'google'
ENABLE  = True
PATTERN = '^!g (?P<query>.*$)'
USAGE   = '''Usage: !g <query>
Given a search query, this returns the first result from Google.
Example:
    > !g who likes short shorts?
'''

# Constants

GOOGLE_API_URL = 'https://customsearch.googleapis.com/customsearch/v1'
GOOGLE_API_KEY = None
GOOGLE_API_CSE = None

# Command

async def google(bot, message, query=None):
    params = {
        'q'  : query,
        'num': 1,
        'key': GOOGLE_API_KEY,
        'cx' : GOOGLE_API_CSE,
    }
    async with bot.http_client.get(GOOGLE_API_URL, params=params) as response:
        try:
            data  = await response.json()
            item  = data['items'][0]
            title = html.unescape(item['title'])
            url   = await shorten_url(bot.http_client, item['link'])
            response = bot.client.format_text(
                '{color}{green}Google{color}: ' +
                '{bold}{title}{bold} @ {color}{blue}{url}{color}',
                title = title,
                url   = url
            )
        except (IndexError, ValueError) as e:
            logging.warning(e)
            response = 'No results'

        return message.with_body(response)

# Register

def register(bot):
    global GOOGLE_API_KEY, GOOGLE_API_CSE

    config         = bot.config.load_module_config('google')
    GOOGLE_API_KEY = config.get('api_key', None)
    GOOGLE_API_CSE = config.get('api_cse', None)

    return (
        ('command', PATTERN, google),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

# wolfram.py

import logging

# Metadata

NAME    = 'wolfram'
ENABLE  = True
PATTERN = '^!wa (?P<query>.*$)'
USAGE   = '''Usage: !g <query>
Given a search query, this returns a short textual answer from Wolfram Alpha.
Example:
    > !wa what is the value of pi
'''

# Constants

WOLFRAM_ALPHA_URL   = 'http://api.wolframalpha.com/v1/result'
WOLFRAM_ALPHA_APPID = None

# Command

async def wolfram(bot, message, query=None):
    params = {
        'i'     : query,
        'appid' : WOLFRAM_ALPHA_APPID,
    }
    async with bot.http_client.get(WOLFRAM_ALPHA_URL, params=params) as response:
        try:
            response = bot.client.format_text(
                '{color}{green}Wolfram Alpha{color}: {bold}{answer}{bold}',
                answer = await response.text()
            )
        except (IndexError, ValueError) as e:
            logging.warning(e)
            response = 'No results'

        return message.with_body(response)

# Register

def register(bot):
    global WOLFRAM_ALPHA_APPID

    config              = bot.config.load_module_config('wolfram')
    WOLFRAM_ALPHA_APPID = config.get('appid', None)

    if not WOLFRAM_ALPHA_APPID:
        return []

    return (
        ('command', PATTERN, wolfram),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

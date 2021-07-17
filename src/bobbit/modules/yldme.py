# yldme.py

import re

from bobbit.utils import shorten_url

# Metadata

NAME    = 'yldme'
ENABLE  = True
PATTERN = r'^!yldme\s*(?P<url>[^\s]*)$'
USAGE   = '''Usage: !yldme <url>
Given a url, return a shortened version.
Example:
    > !yldme https://waifupaste.moe
    https://yld.me/l1X
'''

# Command

async def yldme(bot, message, url=''):
    if not url:
        for m in bot.history.search(message.channel, pattern='http[s]*://', limit=1, reverse=True):
            url = re.findall(r'(http[s]*://[^\s<>]+)', m.body)[0]

    short_url = await shorten_url(bot.http_client, url)
    if short_url != url:
        response = bot.client.format_text('{bold}YldMe{bold}: {url}', url=short_url)
        return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, yldme),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

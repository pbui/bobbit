# yldme.py

import re

from bobbit.utils import shorten_url

# Metadata

NAME    = 'yldme'
ENABLE  = True
PATTERN = '^!yldme (?P<url>[^\s]*)$'
USAGE   = '''Usage: !yldme <url>
Given a url, return a shortened version.
Example:
    > !yldme https://waifupaste.moe
    https://yld.me/l1X
'''

# Command

async def yldme(bot, message, url):
    if url == 'last':
        for m in bot.history.search(message.channel, pattern='http[s]*://', limit=1, reverse=True):
            url = re.findall('(http[s]*://[^\s<>]+)', m.body)[0]

    response = await shorten_url(bot.http_client, url)
    if response != url:
        return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, yldme),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

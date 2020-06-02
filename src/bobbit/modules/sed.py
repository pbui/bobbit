# sed.py

import re

# Metadata

NAME    = 'sed'
ENABLE  = True
PATTERN = '^s/(?P<pattern>[^/]+)/(?P<replacement>[^/]+)[/]*$'
USAGE   = '''Usage: s/pattern/replacement/
This searches the channel's history for the most recent line that has the
pattern and then performs the replacement.
'''

# Command

async def sed(bot, message, pattern, replacement):
    replacement = bot.client.format_text('{bold}{}{bold}', replacement)
    for original in bot.history.search(message.channel, pattern=pattern, limit=1, reverse=True):
        replaced = re.sub(pattern, replacement, original.body)
        return original.copy(body=replaced)

# Register

def register(bot):
    return (
        ('command', PATTERN, sed),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

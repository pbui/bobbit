# slap.py

import random

# Metadata

NAME    = 'slap'
ENABLE  = True
PATTERN = '^!slap (?P<target>.*)'
USAGE   = '''Usage: !slap <target>
This module slaps given target with a random message
Example:
    > !slap jsull
    pnutzh4x0r slaps jsull around a bit with a large trout
'''

# Constants

RESPONSES = (
    "slaps {target} around a bit with a large troutn",
    "gives {target} a clout round the head with a fresh copy of WeeChat",
    "slaps {target} with a large smelly trout",
    "breaks out the slapping rod and looks sternly at {target}",
    "slaps {target}'s bottom and grins cheekily",
    "slaps {target} a few times",
    "slaps {target} and starts getting carried away",
    "would slap {target}, but is not being violent today",
    "gives {target} a hearty slap",
    "finds the closest large object and gives {target} a slap with it",
    "likes slapping people and randomly picks {target} to slap",
    "dusts off a kitchen towel and slaps it at {target}",
)

# Command

async def slap(bot, message, target=None):
    target   = bot.client.format_text('{bold}{target}{bold}', target=target)
    response = random.choice(RESPONSES).format(target=target)

    return message.with_body(bot.client.format_text(
        '{bold}{nick}{bold} {response}', nick=message.nick, response=response
    ))

# Register

def register(bot):
    return (
        ('command', PATTERN, slap),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

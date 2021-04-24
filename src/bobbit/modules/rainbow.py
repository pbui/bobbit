# rainbow.py

import itertools
import random

# Metadata

NAME    = 'rainbow'
ENABLE  = True
PATTERN = r'^!rainbow (?P<phrase>.*)'
USAGE   = '''Usage: !rainbow <phrase>
Given a phrase, this colorizes the text with colors of the rainbow.
Example:
    > !rainbow baby you're a firework!
    baby you're a firework!
'''

# Constants

COLORS = (
    'brown',
    'red',
    'orange',
    'yellow',
    'green',
    'lightgreen',
    'blue',
    'lightblue',
    'cyan',
    'lightcyan',
    'magenta',
    'pink',
)

# Command

async def rainbow(bot, message, phrase):
    colors   = itertools.cycle(COLORS)
    response = ''

    # Cycle through colors a random amount to offset
    for _ in range(random.randrange(len(COLORS))):
        next(colors)

    # Colorize non-space letters
    for letter in phrase:
        if not letter.isspace():
            response += '{color}{' + next(colors) + '}' + letter + '{color}'
        else:
            response += letter

    return message.with_body(
        bot.client.format_text('{bold}' + response + '{bold}')
    )

# Register

def register(bot):
    return (
        ('command', PATTERN, rainbow),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

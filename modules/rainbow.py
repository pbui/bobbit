# rainbow.py

import itertools

# Metadata

NAME    = 'rainbow'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!rainbow (?P<phrase>.*)'
USAGE   = '''Usage: !rainbow <phrase>
Given a phrase, this colorizes the text with colors of the rainbow.
Example:
    > !rainbow baby you're a firework!
    baby you're a firework!
'''

# Constants
# https://github.com/myano/jenni/wiki/IRC-String-Formatting

COLORS = (
    'red',
    'orange',
    'yellow',
    'gold',
    'green',
    'lime',
    'cyan',
    'teal',
    'blue',
    'royal',
    'purple',
    'fuchsia',
)

# Command
def command(bot, nick, message, channel, phrase):
    colors   = itertools.cycle(COLORS)
    response = ''
    for letter in phrase:
        if not letter.isspace():
            response += '{color}{' + next(colors) + '}' + letter + '{color}'
        else:
            response += letter

    response = bot.format_text('{bold}' + response + '{bold}')
    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
	(PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:


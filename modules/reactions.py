# reactions.py

import random

# Metadata

NAME    = 'reactions'
ENABLE  = False
TYPE    = 'command'
PATTERN = '^(?P<phrase>(hott|yes|omg|yay|yeah))$'
USAGE   = '''Usage: <phrase>
This reacts to certain words like hott or yay
'''

# Constants

AGREEMENTS = (
    'totes',
    'ikr',
    'indeed',
    'u betcha',
    'zomg',
    '\o/',
)

# Command

def command(bot, nick, message, channel, phrase=None):
    bot.send_message(random.choice(AGREEMENTS), nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

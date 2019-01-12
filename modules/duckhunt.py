# duckhunt.py

import random
import re
import time

import tornado.ioloop

# Metadata

NAME    = 'duckhunt'
ENABLE  = False
TYPE    = 'command'
PATTERN = re.compile('.*(FLAP|QUACK)!$', re.IGNORECASE)
USAGE   = '''Usage: N/A
This module snipes ducks from gonzobot.
'''

# Constants

SNIPES = ('.bef', '.bang')

# Command

def command(bot, nick, message, channel):
    if nick != 'gonzobot':
        return

    tornado.ioloop.IOLoop.current().add_timeout(
        time.time() + random.randint(1, 5),
        lambda: bot.send_message(random.choice(SNIPES), None, channel))

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

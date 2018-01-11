# greeting.py ------------------------------------------------------------------

import random
import re

# Metadata ---------------------------------------------------------------------

NAME    = 'greeting'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^(hi|hello|hey|greetings|hola|sup)$'
USAGE   = '''Usage: <greeting>
Given a greeting such as hi or hello, this module responds with a similar
greeting.
'''

# Constants --------------------------------------------------------------------

RESPONSES = (
    'hi',
    'hello',
    'sup',
    'greetings',
    'hola',
    'yo',
)

# Command ----------------------------------------------------------------------

def command(bot, nick, message, channel, question=None):
    response = random.choice(RESPONSES)
    bot.send_response(response, nick, channel)

# Register ---------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------

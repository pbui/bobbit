# greeting.py

import random

# Metadata

NAME    = 'greeting'
ENABLE  = True
PATTERN = r'^(hi|hello|hey|greetings|hola|sup|bonjour|ciao|salut)$'
USAGE   = '''Usage: <greeting>
Given a greeting such as hi or hello, this module responds with a random
greeting.
'''

# Constants

RESPONSES = (
    'hi',
    'hello',
    'sup',
    'greetings',
    'hola',
    'yo',
    'bonjour',
)

# Command

async def greeting(bot, message):
    return message.with_body(random.choice(RESPONSES))

# Register

def register(bot):
    return (
        ('command', PATTERN, greeting),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

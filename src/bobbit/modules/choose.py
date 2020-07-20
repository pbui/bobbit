# choose.py

import random

# Metadata

NAME    = 'choose'
ENABLE  = True
PATTERN = '^!choose (?P<options>.*)'
USAGE   = '''Usage: !choose <options>
Given a list of options separated by "or", this chooses one of them.
Example:
    > !choose stay or go
    stay
'''

# Command

async def choose(bot, message, options=None):
    options = options.split(' or ')
    return message.with_body(random.choice(options))

# Register

def register(bot):
    return (
        ('command', PATTERN, choose),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

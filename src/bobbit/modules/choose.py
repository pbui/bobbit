# choose.py

import random

# Metadata

NAME    = 'choose'
ENABLE  = True
PATTERN = '^!choose (?:-b (?P<best_of>[0-9]) )?(?P<options>.*)'
USAGE   = '''Usage: !choose [FLAG] <options>
Given a list of options separated by "or", this chooses one of them.
-b <best_of>
    choose <best_of> times
Example:
    > !choose stay or go
    stay
'''

# Command

async def choose(bot, message, options=None, best_of=None):
    options = options.split(' or ')
    if best_of is None:
        return message.with_body(random.choice(options))
    else:
        choices = ''
        for i in range(0, int(best_of)):
            choices += random.choice(options) + '\n'
        return message.with_body(choices.strip())


# Register

def register(bot):
    return (
        ('command', PATTERN, choose),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

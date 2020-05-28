# expand.py

# Metadata

NAME    = 'expand'
ENABLE  = True
PATTERN = r'^!expand (?P<phrase>.*)'
USAGE   = '''Usage: !expand <phrase>
Given a phrase, this inserts a space between each letter.
Example:
    > !expand social distancing
    s o c i a l   d i s t a n c i n g
'''

# Command

async def expand(bot, message, phrase):
    return ' '.join(list(phrase))

# Register

def register(bot):
    return (
        ('command', PATTERN, expand),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

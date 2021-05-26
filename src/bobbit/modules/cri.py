# lenny.py

import random

# Metadata

NAME = 'cri'
ENABLE = True
PATTERN = r'^![Cc]ri\s*(?P<text>.*)$'
USAGE = '''Usage: ![Cc]ri
Displays a crying lenny face :,(
'''

# Lenny Faces from Gonzobot

CRI = [
    'ಥʖ̯ಥ'
]

# Command

async def cri(bot, message, text=None):
    response = random.choice(CRI)
    if text:
        response += ' ' + text
    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, cri),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
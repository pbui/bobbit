# lenny.py

import random

# Metadata

NAME    = 'lenny'
ENABLE  = True
PATTERN = r'^![Ll]enny\s*(?P<text>.*)$'
USAGE   = '''Usage: ![Ll]enny
Displays a Lenny face ( ͡° ͜ʖ ͡°)
'''

# Lenny Faces from Gonzobot

LENNYS = [
    '( \u0361\u00B0 \u035C\u0296 \u0361\u00B0)',
    '( \u0360\u00B0 \u035F\u0296 \u0361\u00B0)',
    '\u1566( \u0361\xb0 \u035c\u0296 \u0361\xb0)\u1564',
    '( \u0361\u00B0 \u035C\u0296 \u0361\u00B0)',
    '( \u0361~ \u035C\u0296 \u0361\u00B0)',
    '( \u0361o \u035C\u0296 \u0361o)', u'\u0361\u00B0 \u035C\u0296 \u0361 -',
    '( \u0361\u0361 \u00B0 \u035C \u0296 \u0361 \u00B0)\uFEFF',
    '( \u0361 \u0361\u00B0 \u0361\u00B0  \u0296 \u0361\u00B0 \u0361\u00B0)',
    '(\u0E07 \u0360\u00B0 \u035F\u0644\u035C \u0361\u00B0)\u0E07',
    '( \u0361\u00B0 \u035C\u0296 \u0361 \u00B0)',
    '( \u0361\u00B0\u256D\u035C\u0296\u256E\u0361\u00B0 )'
]

# Command

async def lenny(bot, message, text=None):
    response = random.choice(LENNYS)
    if text:
        response += ' ' + text
    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, lenny),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

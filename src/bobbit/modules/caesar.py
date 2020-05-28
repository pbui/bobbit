# caesar.py

import string

# Metadata

NAME    = 'caesar'
ENABLE  = True
PATTERN = '^!caesar (?P<phrase>.*)'
USAGE   = '''Usage: !caesar <phrase>
Given a phrase, this performs a caesar cipher on the phrase
Example:
    > !caesar veni, vidi, vici
    Irqv, irav, ivpv
'''

# Constants

SOURCE  = string.ascii_lowercase
TARGET  = SOURCE[13:] + SOURCE[:13]
SOURCE += SOURCE.upper()
TARGET += TARGET.upper()
CIPHER  = str.maketrans(SOURCE, TARGET)

# Command

async def caesar(bot, message, phrase):
    return message.with_body(phrase.translate(CIPHER))

# Register

def register(bot):
    return (
        ('command', PATTERN, caesar),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

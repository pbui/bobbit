# caesar.py

import string

# Metadata

NAME    = 'caesar'
ENABLE  = True
TYPE    = 'command'
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

def command(bot, nick, message, channel, phrase):
    bot.send_response(phrase.translate(CIPHER), nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

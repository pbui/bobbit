# leetspeak.py

import random

# Metadata

NAME    = 'leetspeak'
ENABLE  = True
PATTERN = '^!leet (?P<phrase>.*)'
USAGE   = '''Usage: !leet <phrase>
Given a phrase, this translates the phrase into leetspeak.
Example:
    > !leet notre dame
    n07r3 d4m3
'''

# Constants

# Mapping from http://en.wikipedia.org/wiki/Leet

_A = ('a', '4', '4', '@', '@')
_C = ('c', 'c', 'c', '(', '<')
_E = ('e', '3', '3', '3')
_L = ('l', '1', '1', '1', '|')
_O = ('o', '0', '0', '0', '()')
_S = ('s', '5', '5', '$', 'z')
_T = ('t', '7', '+', '7', '+')

# Command

async def leetspeak(bot, message, phrase):
    response = phrase.lower().strip()\
                     .replace('a', random.choice(_A))\
                     .replace('c', random.choice(_C))\
                     .replace('e', random.choice(_E))\
                     .replace('l', random.choice(_L))\
                     .replace('o', random.choice(_O))\
                     .replace('s', random.choice(_S))\
                     .replace('t', random.choice(_T))
    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, leetspeak),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

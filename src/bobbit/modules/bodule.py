# clap.py

from bobbit.utils import parse_options

# Metadata

NAME    = 'bodule'
ENABLE  = True
PATTERN = '^![Bb] (?P<phrase>.*)'
USAGE   = '''Usage: !b [-[a-zA-Z0-9]+] <phrase>
Given a phrase, b-ifies every word.

Example:
    > !bodule What's on my mind?
    🅱️hat's 🅱️on 🅱️y 🅱️ind?
'''

# Command

async def bodule(bot, message, phrase):
    phrase   = phrase.rstrip().split()
    response = ''
    vowels   = {'a', 'e', 'i', 'o', 'u'}
    special  = {}

    if phrase[0].startswith('-'):
        special = set(list(phrase.pop(0)[1:]))
        vowels  = vowels & special

    for word in phrase:
        curr = word[0].lower()

        if curr in vowels:
            response += '🅱' + word
        elif curr in special or not special:
            response += '🅱' + word[1:]
        else:
            response += word

        response += ' '

    return message.with_body(response)


# Register

def register(bot):
    return (
        ('command', PATTERN, bodule),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

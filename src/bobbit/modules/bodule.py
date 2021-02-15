# clap.py

from bobbit.utils import parse_options

# Metadata

NAME    = 'bodule'
ENABLE  = True
PATTERN = '^![Bb]odule (?P<phrase>.*)'
USAGE   = '''Usage: !bodule <phrase>
Given a phrase, b-ifies every word.

Example:
    > !bodule What's on my mind?
    🅱️hat's 🅱️on 🅱️y 🅱️ind?
'''

# Command

async def bodule(bot, message, phrase):
    phrase   = phrase.rstrip().split()
    response = ''
    vowels = {'a', 'e', 'i', 'o', 'u'}

    for word in phrase:
        if word[0].lower() in vowels:
            response += '🅱' + word
        else:
            response += '🅱' + word[1:]
        
        response += ' '

    return message.with_body(response)


# Register

def register(bot):
    return (
        ('command', PATTERN, bodule),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

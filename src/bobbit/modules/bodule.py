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
    phrase = phrase.rstrip().split()
    response = ''
    vowels = {'a', 'e', 'i', 'o', 'u'}

    to_replace = None
    if phrase[0].startswith('-'):
        to_replace = phrase.pop(0)[1:]

    for word in phrase:
        if to_replace and word.lower().startswith(to_replace):
            response += '🅱' + word[len(to_replace):] + ' '
            continue
        elif to_replace:
            response += word + ' '
            continue

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

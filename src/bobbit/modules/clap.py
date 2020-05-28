# clap.py

from bobbit.utils import parse_options

# Metadata

NAME    = 'clap'
ENABLE  = True
USAGE   = '''Usage: !clap [-s -r REPLACEMENT] <phrase>
Given a phrase, this replaces all spaces with the clap emoji.

    -s              Surround phrase
    -r REPLACEMENT  The text to put between each word

Example:
    > !clap Do I look like I'm joking
    Do 👏 I 👏 look 👏 like 👏 I'm 👏 joking 👏
'''

# Command

async def clap(bot, message, phrase, replacement='👏'):
    options, phrase = parse_options({'-s': False, '-r': replacement}, phrase)
    replacement     = options['-r']
    surround        = options['-s']
    phrase          = phrase.replace(' ', f' {replacement} ')

    if surround:
        return message.with_body(f'{replacement} {phrase} {replacement}')
    else:
        return message.with_body(phrase)

# Register

def register(bot):
    return (
        ('command', '^!clap (?P<phrase>.*)', clap),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

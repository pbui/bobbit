# clap.py

# Metadata

NAME    = 'clap'
ENABLE  = True
PATTERN = '^!clap (?P<phrase>.*)'
USAGE   = '''Usage: !clap <phrase>
Given a phrase, this replaces all spaces with the clap emoji.
Example:
    > !clap Do I look like I'm joking
    Do U0001F44F I U0001F44F look U0001F44F like U0001F44F I'm U0001F44F joking U0001F44F
'''

# Command

async def clap(bot, message, phrase):
    return message.with_body(phrase.replace(' ', ' \U0001F44F '))

# Register

def register(bot):
    return (
        ('command', PATTERN, clap),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

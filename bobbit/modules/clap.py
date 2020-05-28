# clap.py

# Metadata

NAME    = 'clap'
ENABLE  = True
USAGE   = '''Usage: !clap <phrase>
Given a phrase, this replaces all spaces with the clap emoji.
Example:
    > !clap Do I look like I'm joking
    Do 👏 I 👏 look 👏 like 👏 I'm 👏 joking 👏
'''

# Command

async def clap(bot, message, phrase):
    return message.with_body(phrase.replace(' ', ' 👏 '))

async def crab(bot, message, phrase):
    return message.with_body(phrase.replace(' ', ' 🦀 '))

# Register

def register(bot):
    return (
        ('command', '^!clap (?P<phrase>.*)', clap),
        ('command', '^!crab (?P<phrase>.*)', crab),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

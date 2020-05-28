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
# Utility

def make_clapper(replacement):
    return lambda *args, **kwargs: clap(*args, **kwargs, replacement=replacement)

# Command

async def clap(bot, message, phrase, replacement='👏'):
    return message.with_body(phrase.replace(' ', f' {replacement} '))

# Register

def register(bot):
    return (
        ('command', '^!clap (?P<phrase>.*)', clap),
        ('command', '^!crab (?P<phrase>.*)', make_clapper('🦀')),
        ('command', '^!fire (?P<phrase>.*)', make_clapper('🔥')),
        ('command', '^!tear (?P<phrase>.*)', make_clapper('💧')),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

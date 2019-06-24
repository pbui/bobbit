# rainbow.py

import itertools

# Metadata

NAME    = 'rainbow'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!rainbow (?P<phrase>.*)'
USAGE   = '''Usage: !rainbow <phrase>
Given a phrase, this colorizes the text with colors of the rainbow.
Example:
    > !rainbow baby you're a firework!
    baby you're a firework!
'''
# Constants
# https://github.com/myano/jenni/wiki/IRC-String-Formatting

COLORS = (
    '04',   # Red
    '07',   # Orange
    '08',   # Yellow
    '03',   # Green
    '09',   # Lime
    '10',   # Teal
    '11',   # Cyan
    '02',   # Blue
    '12',   # Royal
    '06',   # Purple
    '13',   # Fuchsia
)

# Command
def command(bot, nick, message, channel, phrase):
    colors   = itertools.cycle(COLORS)
    response = ''
    for letter in phrase:
        if not letter.isspace():
            response += '\x02\x03{}{}\x03\x02'.format(next(colors), letter)
        else:
            response += letter

    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
	(PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:


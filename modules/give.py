# give.py

from modules.__common__ import PrefixedNick

# Metadata

NAME    = 'give'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!give (?P<other>[^\s]*) (?P<phrase>.*)'
USAGE   = '''Usage: !give <nick> <phrase>
Send specified nick the result of the given phrase.
Example:
    > !give bobbit !8ball does this work?
    bobbit: Don't count on it
'''

# Command

def command(bot, nick, message, channel, other, phrase=None):
    bot.process_command(PrefixedNick(other), phrase, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

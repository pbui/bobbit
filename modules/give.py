# give.py

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

# Class

class Nick(str):
    def __new__(cls, content):
        self = super().__new__(cls, content)
        self.prefix = True
        return self

# Command

def command(bot, nick, message, channel, other, phrase=None):
    nick = Nick(other)
    bot.process_command(nick, phrase, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

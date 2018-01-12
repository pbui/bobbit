# give.py ----------------------------------------------------------------------

# Metadata ---------------------------------------------------------------------

NAME    = 'give'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!give (?P<other>[^\s]*) (?P<message>.*)'
USAGE   = '''Usage: !give <nick> <message>
Send specified nick the result of the given message.
Example:
    > !give bobbit !8ball does this work?
    bobbit: Don't count on it
'''

# Command ----------------------------------------------------------------------

def command(bot, nick, message, channel, other, message=None):
    bot.process_command(other, message, channel)

# Register ---------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------

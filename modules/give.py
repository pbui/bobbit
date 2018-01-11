# give.py ----------------------------------------------------------------------

# Meta-data --------------------------------------------------------------------

NAME    = 'give'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!give (?P<other>[^\s]*) (?P<command>.*)'
USAGE   = '''Usage:  !give <nick> <command>
Send specified nick the result of the given command.
Example:
    > !give bobbit !8ball does this work?
    bobbit: Don't count on it
'''

# Command ----------------------------------------------------------------------

def command(bot, nick, message, channel, other, command=None):
    for response in bot.process_command(other, command, channel):
        if response:
            bot.send_response(response, channel=channel)
    return None

# Register ---------------------------------------------------------------------

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------

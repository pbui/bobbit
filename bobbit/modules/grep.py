# grep.py

# Metadata

NAME    = 'grep'
ENABLE  = True
PATTERN = r'^!grep\s+(?P<pattern>.*)$'
USAGE   = '''Usage: !grep pattern
This searches the channel's history for the specified pattern.
'''

# Command

async def grep(bot, message, pattern):
    # TODO: Highlight matched part
    # TODO: Add support for -n nick
    return [m for m in bot.history.search(message.channel, pattern=pattern)]

# Register

def register(bot):
    return (
        ('command', PATTERN, grep),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

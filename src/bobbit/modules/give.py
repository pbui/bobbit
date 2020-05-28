# give.py

# Metadata

NAME    = 'give'
ENABLE  = True
PATTERN = r'^!give (?P<other>[^\s]*) (?P<phrase>.*)'
USAGE   = '''Usage: !give <nick> <phrase>
Send specified nick the result of the given phrase.
Example:
    > !give bobbit !8ball does this work?
    bobbit: Don't count on it
'''

# Command

async def give(bot, message, other, phrase=None):
    message = message.copy(body=phrase, nick=other, highlighted=True)
    async for response in bot.process_message(message):
        if response:        # NOTE: return first valid response
            return response

# Register

def register(bot):
    return (
        ('command', PATTERN, give),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

# dirc.py

from bobbit.message import Message

# Metadata

NAME    = 'dirc'
ENABLE  = True
PATTERN = r'^<(?P<nick>[^>]+)> (?P<phrase>.*)'
USAGE   = '''Usage: <nick> phrase
Intercepts messages from dirc discord bot and processes as normal IRC
messages.
'''

# Command

async def dirc(bot, message, nick, phrase=None):
    if message.nick != 'dirc':
        return

    message   = message.copy(body=phrase, nick=nick)
    responses = []
    async for response in bot.process_message(message):
        if isinstance(response, Message):
            responses.append(response)
        elif isinstance(response, list):
            responses.extend(response)
    return responses

# Register

def register(bot):
    return (
        ('command', PATTERN, dirc),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

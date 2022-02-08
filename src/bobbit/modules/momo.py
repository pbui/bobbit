# momo.py

from bobbit.message import Message

# Metadata

NAME    = 'momo'
ENABLE  = True
PATTERN = r'^\[(?P<world>[^\]]+)\] <(?P<player>[^>]+)> (?P<phrase>.*)'
USAGE   = '''Usage: [world] <player> phrase 
Intercepts messages from momo Minecraft bot and processes as normal IRC
messages.
'''

# Command

async def momo(bot, message, world, player, phrase=None):
    if message.nick != 'momo':
        return

    message   = message.copy(body=phrase, nick=player)
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
        ('command', PATTERN, momo),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

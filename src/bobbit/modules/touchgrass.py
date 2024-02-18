# touchgrass.py

# Metadata

NAME = 'touchgrass'
ENABLE = True
PATTERN = r'!touchgrass (?P<nick>[^\s]+)'
USAGE = '''Usage: !touchgrass <nick>
This informs the user identified by the nick that they should go outside and touch grass
'''

#Command

async def touchgrass(bot, message, nick):
    if nick not in bot.users:
        return message.with_body(f'Unknown nick {nick}, maybe they\'re outside?')
    else:
        return message.with_body(f'{message.nick} thinks you should go outside and touch some grass, {nick}. Perhaps take a shower while your up')

# Register

def register(bot):
    return (('command', PATTERN, touchgrass),)

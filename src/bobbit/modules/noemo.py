# noemo.py

# Metadata

NAME = 'noemo'
ENABLE = True
PATTERN = r'!noemo (?P<nick>[^\s]+)'
USAGE = '''Usage: !noemo <nick>
This informs the user identified by the nick that they should no longer be emo, it's depressing
'''

#Command

async def noemo(bot, message, nick):
    if nick not in bot.users:
        return message.with_body(f'Unknown nick: {nick}, give them a hug for me')
    else:
        return message.with_body(f'{message.nick} thinks you shouldn\'t be so emo, {nick}. Take a deep breath and lighten up')

# Register

def register(bot):
    return (
            ('command', PATTERN, noemo),)

# tell.py

# Metadata

NAME    = 'tell'
PATTERN = r''
ENABLE  = True
USAGE   = '''Usage: !tell <user> <message>
This queues a message to send to a user the next time they are active (ie.
the next time they send a message).
'''

# Command

async def tell(bot, message):
    # Saving
    if message.body.startswith("!tell"):
        targets, body = message.body[5:].split(maxsplit=1)

        for target in targets.split(','):
            if target not in bot.users:
                bot.users[target] = {}

            saved_message = message.nick + ": " + body

            try:
                bot.users[target]['mailbox'].append(saved_message)
            except KeyError:
                bot.users[target]['mailbox'] = [saved_message]

    # Sending
    if message.nick in bot.users and bot.users[message.nick].get('mailbox', []):
        message.channel = None # Make Message a PM/Notice
        to_tell = [
            message.copy(body=f'Message from {msg}', notice=True)
            for msg in bot.users[message.nick]['mailbox']
        ]
        del bot.users[message.nick]['mailbox']
        return to_tell

# Register

def register(bot):
    return (
        ('command', PATTERN, tell),
    )

# tell.py

from collections import defaultdict

# Metadata
NAME    = 'tell'
PATTERN = r''
ENABLE  = True
USAGE   = '''Usage: !tell <user> <message>
This queues a message to send to a user the next time they are active (ie.
the next time they send a message).
'''

MAILBOX = defaultdict(list)

# Command

async def tell(bot, message):
    if message.body.startswith("!tell"):
        target, *body = message.body[5:].split()
        MAILBOX[target].append(message.nick + ": " + ' '.join(body))

    if message.nick in MAILBOX:
        to_tell = [message.copy(body=f'Tell from {msg}', channel=None, notice=True) for msg in MAILBOX[message.nick]]
        del MAILBOX[message.nick]
        return to_tell

# Register

def register(bot):
    return (
        ('command', PATTERN, tell),
    )

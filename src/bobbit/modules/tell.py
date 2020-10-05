# tell.py

import logging

# Metadata
NAME    = 'tell'
PATTERN = r'.*'
ENABLE  = True
USAGE   = '''Usage: !tell <user> <message>
This queues a message to send to a user the next time they are active (ie.
the next time they send a message).
'''

MAILBOX = {}

# Functions

def tell_handle(bot, message):
    if message.body.startswith("!tell"):
        tell_message = message.body[5:].split()
        if tell_message[0] in MAILBOX:
            MAILBOX[tell_message[0]].append(tell_message[0] + ": " + ' '.join(tell_message[1:]))
        else:
            MAILBOX[tell_message[0]] = [tell_message[0] + ": " + ' '.join(tell_message[1:])]

    if message.nick in MAILBOX:
        to_tell = [message.with_body(f'Tell from {msg}') for msg in MAILBOX[message.nick]]
        del MAILBOX[message.nick]
        return to_tell

# Command

async def tell(bot, message):
    return tell_handle(bot, message)

# Register

def register(bot):
    return (
        ('command', PATTERN, tell),
    )

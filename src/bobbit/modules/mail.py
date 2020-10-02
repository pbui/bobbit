# mail.py

import time

# Metadata
NAME    = 'mail'
PATTERN = r'^!mail\s+(?P<user>[^\s]*) (?P<mail_body>.*)$'
ENABLE  = True
USAGE   = '''Usage: !mail <user> <message>
This queues a message to send to a user the next time they are active (ie.
the next time they send a message).
'''

# Functions

def send_mail_messages(bot, message, user):
    for msg in bot.mailbox[user]:
        return message.with_body(f'Mail from {msg}')

def discard_mail_messages(bot, user):
    del bot.mailbox[user]

async def mail(bot, message, user, mail_body):
    mail_body = message.nick + ": " + mail_body
    if user in bot.mailbox:
        bot.mailbox[user].append(mail_body)
    else:
        bot.mailbox[user] = [mail_body]
# Register

def register(bot):
    return (
        ('command', PATTERN, mail),
    )

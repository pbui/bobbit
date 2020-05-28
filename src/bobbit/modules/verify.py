# verify.py

import base64
import hashlib
import random

# Metadata

NAME    = 'verify'
ENABLE  = True
PATTERN = r'^!verify (?P<netid>[^\s]*) (?P<passcode>.*)'
USAGE   = '''Usage: !verify netid passcode
Given a netid and passcode, this will verify the drop.
Example:
    > !verify pbui 1cc8de27f54ab8f6ab92706354d483e5e5efc6d1
'''

# Constants

ROT13         = str.maketrans('ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
                              'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')
GREETINGS     = ('hey', 'bonjour', 'hi', 'hello', 'greetings', 'hola')
FAILURES      = (
    'Pardonez moi?',
    "No Puppet... No Puppet... You're the Puppet",
    "Are your some 400 lb hacker or something?",
    "Bzzt",
    "How about no",
    "Some people choose to see the ugliness in this world. The disarray. I choose to see the beauty.",
    "I'm sorry, I'm afraid I can't do that",
    "Segmentation Fault",
)
SUCCESSES    = (
    "Welcome to the Party",
    "Authentication Verified",
    "Access Granted",
    "With great power, comes great responsibility",
)

# Functions

def cksum(s):
    return hashlib.sha1(s.encode()).hexdigest()

def rot13(s):
    return str.translate(s, ROT13)

# Command

async def verify(bot, message, netid, passcode):
    if message.highlighted:
        return

    if passcode == base64.b64encode((netid + '\n').encode()).decode():
        '''
        message  = rot13('{}={}'.format(netid, int(time.time()))).encode()
        response = '{} {}! Please tell the ORACLE the following MESSAGE: {}'.format(
            random.choice(GREETINGS).title(),
            netid,
            base64.b64encode(message).decode(),
        )
        '''
        response = bot.client.format_text(
            '{color}{green}Verify{color}: {}',
            random.choice(SUCCESSES)
        )
    else:
        response = bot.client.format_text(
            '{color}{red}Verify{color}: {}',
            random.choice(FAILURES)
        )

    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, verify),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

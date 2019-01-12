# cksums.py

import hashlib

# Metadata

NAME    = 'cksums'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!(?P<cksum>(md5|sha1)) (?P<phrase>.*)'
USAGE   = '''Usage: !(md5|sha1|sha256) <phrase>
Given a phrase, this returns the cksum of the phrase using the specified algorithm.
Example:
    > !md5 all your base are belong to us
    847dbeb849668d30722d8a67bced1c59
'''

# Constants

CKSUMS = {
    'md5'   : lambda s: hashlib.md5(s.encode()).hexdigest(),
    'sha1'  : lambda s: hashlib.sha1(s.encode()).hexdigest(),
    'sha256': lambda s: hashlib.sha256(s.encode()).hexdigest(),
}

# Command

def command(bot, nick, message, channel, cksum, phrase):
    bot.send_response(CKSUMS[cksum](phrase), nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

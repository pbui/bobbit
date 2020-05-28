# cksums.py

import hashlib

# Metadata

NAME    = 'cksums'
ENABLE  = True
PATTERN = '^!(?P<cksum>(md5|sha1|sha256)) (?P<phrase>.*)'
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

async def cksums(bot, message, cksum, phrase):
    return message.with_body(CKSUMS[cksum](phrase))

# Register

def register(bot):
    return (
        ('command', PATTERN, cksums),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

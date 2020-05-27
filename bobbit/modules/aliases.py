# aliases.py

'''
# Configuration

Store aliases in aliases.yaml file in bobbit configuration directory:

    # Distrowatch aliases
    Arch:     '!distrowatch arch'
    Fedora:   '!distrowatch fedora'
    FerenOS:  '!distrowatch ferenos'
    Solus:    '!distrowatch solus'
    Ubuntu:   '!distrowatch ubuntu'
    Void:     '!distrowatch void'

    # Google aliases
    so:       '!g site:stackoverflow.com'
    nd:       '!g site:nd.edu'

    # Reddit aliases
    riseup:   '!reddit gamersriseup'
'''

# Metadata

NAME    = 'alias'
ENABLE  = True
PATTERN = r'^!(?P<alias>[^ ]+)\s*(?P<arguments>.*)'
USAGE   = '''Usage: !alias
'''

# Constants

ALIASES = {}

# Command

async def aliases(bot, message, alias=None, arguments=None):
    try:
        body = '{} {}'.format(ALIASES[alias], arguments or '').rstrip()
    except KeyError:
        return

    async for response in bot.process_message(message.with_body(body)):
        return response

# Register

def register(bot):
    global ALIASES

    ALIASES = bot.config.load_module_config('aliases')

    return (
        ('command', PATTERN, aliases),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

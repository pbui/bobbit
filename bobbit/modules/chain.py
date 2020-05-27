# chain.py

import logging

from bobbit.message import Message

# Metadata

NAME    = 'chain'
ENABLE  = True
PATTERN = '^!chain (?P<phrase>.*)'
USAGE   = '''Usage: !chain <phrase>
Chain a series or commands (from left-to-right).
Example:
    > !chain !mock !rainbow baby you're a firework
'''

# Command

async def chain(bot, message, phrase=None):
    # Split commands from phrase until we find first non-command
    commands = []
    while phrase.startswith('!'):
        try:
            command, phrase = phrase.split(' ', 1)
        except ValueError:
            command = phrase
            phrase  = ''
        commands.append(command)

    logging.debug('commands: %s, phrase: %s', commands, phrase)

    # Process each command with the result of the previous command
    response = None
    for command in commands:
        message = message.copy(body=f'{command} {phrase}')
        async for responses in bot.process_message(message):
            # NOTE: Some commands return strings, others return Messages
            # NOTE: Must check that the response is valid
            if not responses:
                continue

            if isinstance(responses, list):
                response = responses[0] # TODO: Doesn't work for multi-line responses
            else:
                response = responses

            phrase = response.body if isinstance(response, Message) else response
            break

        response = phrase

    # Return last response
    return response

# Register

def register(bot):
    return (
        ('command', PATTERN, chain),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

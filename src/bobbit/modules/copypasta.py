# copypasta.py

'''
Module for bobbit that pulls posts from r/copypasta. I don't claim any
responsibility for the content of the posts.
-- Gavin Inglis
'''

import random

# Metadata

NAME    = 'copypasta'
ENABLE  = True
PATTERN = '^!copypasta\s*$'
USAGE   = '''Usage: !copypasta
Displays a random post from r/copypasta

WARNING: can be pretty offcolor. Use at your own discretion
'''

# Constants

PASTA_SAUCE   = 'https://www.reddit.com/r/copypasta/.json'
PASTA_MIN_LEN = 0
PASTA_MAX_LEN = 512 # NOTE: Tweet-length

# Command

async def command(bot, message):
    async with bot.http_client.get(PASTA_SAUCE) as response:
        try:
            json_data = await response.json()
            pastas    = []
            for result in json_data['data']['children']:
                data  = result['data']
                pasta = data['selftext'].replace('\r', '').replace('\n', ' ')

                # Ignore long posts b/c IRC
                if PASTA_MIN_LEN < len(pasta) < PASTA_MAX_LEN:
                    pastas.append(pasta)

            response = random.choice(pastas)
        except (IndexError, KeyError, ValueError) as e:
            bot.logger.warn(e)
            response = 'No results'

    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

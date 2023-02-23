# emojify.py
# Author: Evan Day
# Inspired by https://emojify.net/ by Mark Farnum

import json
import random
from bobbit import bot, http_client, message

# Metadata

NAME    = 'emojify'
ENABLE  = True
PATTERN = '^!emojify\s*(?P<phrase>.*)$'
USAGE   = '''Usage: !emojify <phrase>
    Given a phrase, adds emojis.   
Example:
    > !emojify A computer once beat me at chess, but it was no match for me at kick boxing.
    A computer 👩‍💻 once 🔂 beat 🥊🍑 me 😐 at chess, but 🤔 it was no 🚫❌ match 🔥 for 😘 me 🙋 at kick 👞 boxing.
'''

# Globals

EMOJI_TABLE_URL = 'https://raw.githubusercontent.com/farkmarnum/emojify/main/src/data/emoji-data.json'
COMMON_WORDS = set([
  'a',
  'an',
  'as',
  'is',
  'if',
  'of',
  'the',
  'it',
  'its',
  'or',
  'are',
  'this',
  'with',
  'so',
  'to',
  'at',
  'was',
  'and',
])

# Command

async def emojify(bot: bot.Bobbit, message: message.Message, phrase: str):
    async with bot.http_client.get(EMOJI_TABLE_URL) as response:
        if not response.ok:
            return message.with_body('emojify: HTTP request failed :(')
        emojis = json.loads(await response.text())

    result = ''

    for word in phrase.split():
        key = word.strip().lower()
        if key in emojis and key not in COMMON_WORDS:
            options    = list(emojis[key].keys())
            weights    = map(float, emojis[key].values())

            emoji: str = random.choices(options, weights, k=1)[0]

            result += f'{word} {emoji.strip()} '
        else:
            result += f'{word} '

    return message.with_body(result)

# Register

def register(bot):
    return (
        ('command', PATTERN, emojify),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

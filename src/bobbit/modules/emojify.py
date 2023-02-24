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

async def get_emoji_match(emoji_table: dict, word: str):    
    word = word.strip().lower()

    if word in COMMON_WORDS:
        return None

    if word not in emoji_table:
        return None
    
    matches: dict = emoji_table[word]

    options       = list(matches.keys())
    weights       = map(float, matches.values())

    return random.choices(options, weights, k=1)[0]

async def emojify(bot: bot.Bobbit, msg: message.Message, phrase: str):   
    if not phrase:
        return [message.Message(
                    body    = ln,
                    nick    = bot.config.nick,
                    channel = msg.channel
                ) for ln in USAGE.split('\n') if ln.strip()]
    
    try:
        async with bot.client.get(EMOJI_TABLE_URL) as response:      
            emojis = json.loads(await response.text()) 
    except http_client.aiohttp.ClientError:
        return msg.with_body('emojify: couldn\'t fetch emoji table')
    except json.JSONDecodeError:
        return msg.with_body('emojify: couldn\'t parse emoji table')

    result = ''

    for word in phrase.split():
        result += f'{word} '

        if emoji := await get_emoji_match(emojis, word):
             result += f'{emoji} '

    return msg.with_body(result)

# Register

def register(bot):
    return (
        ('command', PATTERN, emojify),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

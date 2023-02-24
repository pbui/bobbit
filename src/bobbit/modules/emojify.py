# emojify.py
# Author: Evan Day
# Inspired by https://emojify.net/ by Mark Farnum

import json
import random
from bobbit import bot, http_client, message

# Metadata

NAME    = 'emojify'
ENABLE  = True
PATTERN = r'^!emojify\s*(?P<flag>-[a-zA-Z]+)?\s*(?P<arg>.*)$'
USAGE   = '''Usage: !emojify [<nick>|-p <phrase>] [-h]
    emojify takes the most recent message and adds emojis to it
    [optional]
    - you can specify the nick of a certain user to emoijfy their most recent message
    - you can use the -p flag to specify your own message
Examples:
    >>> !emojify
    can 🏃🏽‍♂️🏃🏽‍♂️🏃🏽‍♂️ you 👈 push ❗🏽 the branch 🌳 to github?
    >>> !emojify Danielle Croft
    Hey 😡 guys 👨😇👍 don't forget 👋🏾 to periodically check ☑️ in 💘😜 on 🔛 your 👉
    open 😰 pull 💦✊✊😤😣💦🐙 requests! Oftentimes we 👩‍👩‍👦‍👦 will 🙏👊 leave 👎🛫
    comments on ☹️ how 🤐 to fix/improve your 👉👩🏿 programs 📺 so make 👸📓 sure 👍👍🏻
    to keep 🏃‍♀️🏃‍♀️🏃‍♀️🏃‍♀️ an eye 😍 on ⬇️ that!
    >>> !emojify -p A computer once beat me at chess, but it was no match for me at kick boxing.
    A computer 👩‍💻 once 🔂 beat 🥊🍑 me 😐 at chess, but 🤔 it was no 🚫❌ match 🔥 for 😘
    me 🙋 at kick 👞 boxing.
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

FLAGS = ['-p','-h']

# Command    

def get_emoji_match(emoji_table: dict, word: str):
    word = ''.join(let for let in word.strip().lower() if let.isalpha())

    if word in COMMON_WORDS:
        return None

    if word not in emoji_table:
        return None
    
    matches: dict = emoji_table[word]

    options = list(matches.keys())
    weights = map(float, matches.values())

    return random.choices(options, weights, k=1)[0]

def add_emojis(text: str, emoji_table):
    result = ''

    for word in text.split():
        result += f'{word} '

        if emoji := get_emoji_match(emoji_table, word):
             result += f'{emoji} '

    return result.strip()

def error_message(bot, channel, error_message):
    return message.Message(
                body    = error_message,
                nick    = bot.config.nick,
                channel = channel)

async def emojify(bot: bot.Bobbit, msg: message.Message, flag: str, arg: str):
    # check for -h or improper usage and print USAGE
    if flag == '-h' or flag and flag not in FLAGS:
        return [message.Message(
                    body    = ln,
                    nick    = bot.config.nick,
                    channel = msg.channel) for ln in USAGE.split('\n') if ln.strip()]
    
    # parse arguments
    if not flag and not arg:
        # emojify most recent message
        try:
            text = next(bot.history.search(
                            channel=msg.channel,
                            pattern='.',
                            reverse=True
                        )).body
        except StopIteration:
            return error_message(bot, msg.channel, 'emojify: could not find any messages'),
    elif flag == '-p':
        # emojify the arg text
        if not arg:
            return error_message(bot, msg.channel, 'emojify: please specify a phrase')
        
        text = arg
    else:
        # emojify most recent message from nick
        target_nick = arg.split()[0]

        if target_nick not in bot.users:
            return error_message(bot, msg.channel, f'emojify: user {target_nick} not found')
        
        try:
            text = next(bot.history.search(
                            channel=msg.channel,
                            nick=target_nick,
                            reverse=True)).body
        except StopIteration:
            return error_message(bot, msg.channel,
                    f'emojify: could not find a message from {target_nick}')

    # fetch emoji table
    try:
        async with bot.http_client.get(EMOJI_TABLE_URL) as response:      
            emoji_table = json.loads(await response.text()) 
    except http_client.aiohttp.ClientError:
        return error_message(bot, msg.channel, 'emojify: couldn\'t fetch emoji table')
    except json.JSONDecodeError:
        return error_message(bot, msg.channel, 'emojify: couldn\'t parse emoji table')

    return msg.with_body(add_emojis(text, emoji_table))

# Register

def register(bot):
    return (
        ('command', PATTERN, emojify),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

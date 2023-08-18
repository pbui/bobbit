# duckhunt.py

''' Duck Hunt

Todo:
[ ] Add colors
[X] Implement gun jamming / reloading
[ ] Add more messages
[ ] Make kill/save commands configurable
[x] Make channels configurable
[ ] Fix plural
[ ] Add more anti-cheating measures
'''

import random
import time

from bobbit.message import Message
from bobbit.utils   import elapsed_time

# Metadata

NAME    = 'duckhunt'
ENABLE  = True
PATTERN = r'^[\.!](?P<command>(ducks|bang|bef))\s*(?P<other>[^\s]*)$'
USAGE   = '''Usage: ![ducks|bang|bef]
'''

# Constants

DUCK_TAIL   = "・゜゜・。。・゜゜"
DUCK_BODIES = ("\_o< ", "\_O< ", "\_0< ", "\_\u00f6< ", "\_\u00f8< ", "\_\u00f3< ")
DUCK_NOISES = ("QUACK!", "FLAP FLAP!", "quack!")

KILL_MISSES = (
    'WHOOSH! You missed the duck completely!',
    'Your gun jammed!',
    'Better luck next time.',
    'WTF!? Who are you, Dick Cheney?'
)
SAVE_MISSES = (
    "The duck didn't want to be friends, maybe next time.",
    "Well this is awkward, the duck needs to think about it.",
    "The duck said no, maybe bribe it with some pizza? Ducks love pizza don't they?",
    "Who knew ducks could be so picky?"
)
COOLDOWN_AMOUNT = 7.0
COOLDOWN_MESSAGE = f'You can try again in {COOLDOWN_AMOUNT} seconds.'

# Globals

Ducks      = {}         # Release times of active ducks
Times      = {}         # Time thresholds on when to release the next duck
Cooldowns  = {}         # Per-channel cooldowns for users who miss
ReleaseMin = 5*60       # Minimum amount of time before releasing a duck (5 minutes)
ReleaseMax = 2*60*60    # Maximum amount of time before releasing a duck (2 hours)

# Functions

def make_duck():
    pivot = random.randint(1, len(DUCK_TAIL) - 1)
    tail  = DUCK_TAIL[:pivot] + '\u200b' + DUCK_TAIL[pivot:]
    body  = random.choice(DUCK_BODIES)
    noise = random.choice(DUCK_NOISES)
    return ''.join([tail, body, noise])

# Command

async def ducks(bot, message, command, other=None):
    nick         = message.nick
    channel      = message.channel
    current_time = time.time()

    # Add user if not already in database
    if nick not in bot.users:
        bot.users[nick] = {}

    if command == 'ducks':
        if other:
            nick = other

        # Check if user has interacted with ducks
        if 'ducks' not in bot.users[nick]:
            return message.copy(body=f"{nick} hasn't interacted with any ducks!")

        # Report user's statistics
        kills    = bot.users[nick].get('ducks', {}).get('kills', 0)
        saves    = bot.users[nick].get('ducks', {}).get('saves', 0)
        response = f'{nick} has banged {kills} ducks and befriended {saves} ducks.'
        return message.with_body(response)

    if command in ('bang', 'bef'):
        # Check that channel has ducks
        if channel not in Ducks:
            return message.copy(body=f'No ducks are scheduled to visit {channel}.')
        if not Ducks[channel]:
            return message.copy(body=f'There are currently no ducks in {channel}.')

        # Check the cooldown
        if Cooldowns.get(channel, {}).get(nick, 0) > current_time:
            return Message(
                body    = f'You are still on cooldown. You can try again in {elapsed_time(Cooldowns[channel][nick], current_time)}.',
                nick    = nick,
                channel = None,
                notice  = True)

        # Check time (anti-bot) and random chance of missing
        elapsed = current_time - Ducks[channel]
        if elapsed < 1.0 or random.random() > 0.85:
            # Give them a timeout.
            Cooldowns[channel][nick] = current_time + COOLDOWN_AMOUNT
            return message.with_body(' '.join([
                random.choice(KILL_MISSES) if command == 'bang' else random.choice(SAVE_MISSES),
                COOLDOWN_MESSAGE
            ]))

        # Update user stats
        kills = bot.users[nick].get('ducks', {}).get('kills', 0)
        saves = bot.users[nick].get('ducks', {}).get('saves', 0)
        if command == 'bang':
            action = 'banged'
            kills += 1
        else:
            action = 'befriended'
            saves += 1

        # Record user status
        bot.users[nick].update({
            'ducks': {'kills': kills, 'saves': saves}
        })

        # Report action
        elapsed  = elapsed_time(current_time, Ducks[channel])
        response = f'{nick} {action} a duck in {elapsed}!'

        # Reset ducks (0 is not active), set new future release time
        Ducks[channel] = 0
        Times[channel] = current_time + random.randint(ReleaseMin, ReleaseMax)
        return message.with_body(response)

# Timer

async def release(bot):
    current_time = time.time()
    for channel, release_time in Ducks.items():
        # If there is a release time (already active) or if we haven't reached
        # threshold, then don't release a duck
        if release_time or current_time < Times.get(channel, 0):
            continue

        # Record release time and send a message
        Ducks[channel] = current_time
        await bot.outgoing.put(Message(
            channel = channel,
            body    = make_duck(),
        ))

# Register

def register(bot):
    global ReleaseMin, ReleaseMax

    config = bot.config.load_module_config('duckhunt')

    # Check if disabled
    if config.get('disabled', False):
        return []

    # Add channels specified by configuration
    for channel in config.get('channels', []):
        Times[channel]     = 0
        Ducks[channel]     = 0
        Cooldowns[channel] = {}

    # How often to check for release (30 seconds is default)
    release_timeout = config.get('release_timeout', 30)
    ReleaseMin      = config.get('release_min'    , ReleaseMin)
    ReleaseMax      = config.get('release_max'    , ReleaseMax)

    return (
        ('command', PATTERN, ducks),
        ('timer'  , release_timeout, release),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

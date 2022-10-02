# duckhunt.py

''' Duck Hunt

Todo:
[ ] Add colors
[ ] Implement gun jamming / reloading
[ ] Add more messages
[ ] Make kill/save commands configurable
[ ] Make channels configurable
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
PATTERN = r'^!(?P<command>(ducks|bang|bef))$'
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
COOLDOWN_MESSAGE = f" You can try again in {COOLDOWN_AMOUNT}seconds."

# Globals

Times = {   # Time thresholds on when to release the next duck
    '#lug': 0
}

Cooldowns = {
    '#lug': {}
}

Ducks = {   # Release times of active ducks
    '#lug': 0
}

# Functions

def make_duck():
    pivot = random.randint(1, len(DUCK_TAIL) - 1)
    tail  = DUCK_TAIL[:pivot] + '\u200b' + DUCK_TAIL[pivot:]
    body  = random.choice(DUCK_BODIES)
    noise = random.choice(DUCK_NOISES)
    return ''.join([tail, body, noise])

# Command

async def ducks(bot, message, command):
    nick         = message.nick
    channel      = message.channel
    current_time = time.time()

    # Add user if not already in database
    if nick not in bot.users:
        bot.users[nick] = {}

    if command == 'ducks':
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
            return message.copy(body=f"No ducks are scheduled to visit {channel}.")
        if not Ducks[channel]:
            return message.copy(body=f"There are currently no ducks in {channel}.")
        
        # Check the cooldown
        if Cooldowns[channel].get(nick, 0) > current_time:
            return message.copy(body=f"You are still on cooldown. You can try again in {Cooldowns[channel][nick] - current_time} seconds.")


        # Check time (anti-bot) and random chance of missing
        elapsed = current_time - Ducks[channel]
        if elapsed < 1.0 or random.randint(1, 10) > 6:
            # Give them a timeout.
            Cooldowns[channel][nick] = current_time + COOLDOWN_AMOUNT
            return message.with_body(
                random.choice(KILL_MISSES) + COOLDOWN_MESSAGE if command == 'bang' else random.choice(SAVE_MISSES) + COOLDOWN_MESSAGE)

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
        Times[channel] = current_time + random.randint(5*60, 2*60*60)
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
    return (
        ('command', PATTERN, ducks),
        ('timer'  , 30, release),  # TODO
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

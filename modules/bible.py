# bible.py

import random
import re

# Metadata

NAME    = 'bible'
ENABLE  = True
TYPE    = 'command'
PATTERN = re.compile('^!bible$')

USAGE   = '''Usage: !bible
Displays a bible quote from a predefined list
'''

# Command

QUOTES = (
    "'A young man was following Him, wearing nothing but a linen sheet over" \
        + " his naked body; and they seized him. But he pulled free of the " \
        + "linen sheet and escaped naked.' -- Mark 14:51-52",
    "'As a dog returns to its vomit, so a fool repeats his folly.' -- " \
        + "Proverbs 27:15-16",
    "'But Rabshekeh said, Hath my master sent me to thy master and to thee " \
        + "to speak these words? Hath he not sent me to the men that sit upon" \
        + " the wall, that they may eat their own dung, and drink their own " \
        + "piss with you?' -- Isaiah 36:12",
    "'Give beer to those who are perishing, wine to those who are in anguish."\
        + "' -- Proverbs 31:6",
    "'He said to Jacob, Let me eat some of that red stuff, because I'm " \
        + "exhausted.' -- Genesis 25:30",
    "'I wish those who unsettle you would castrate themselves!' -- Galatians "\
        + "5:12",
    "'If a man loudly blesses his neighbor early in the morning, it will be " \
        "taken as a curse.' -- Proverbs 27:14",
    "'If only you would be altogether silent! For you, that would be " \
        + "wisdom.' -- Job 13:5",
    "'No one whose testicles are crushed or whose penis is cut off shall be " \
        + " admitted to the assembly of the LORD.' -- Deuteronomy 23:1",
    "'Thou shalt not boil a kid in its mother's milk.' -- Exodus 23:19",
    "'You shall eat the flesh of your sons, and you shall eat the flesh of " \
        + "your daughters.' -- Leviticus 26:29",
    "'You shall not eat anything which dies of itself. You may give it to the"\
        + " alien who is in your town, so that he may eat it, or you may sell" \
        + " it to a foreigner, for you are a holy people to the LORD your " \
        + "God. -- Deuteronomy 14:21",
)

# Command
def command(bot, nick, message, channel, question=None):
    response = random.choice(QUOTES)
    bot.send_response(response, nick, channel)

# Register
def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set std=4 sw=4 ts=8 expandtab ft=python:

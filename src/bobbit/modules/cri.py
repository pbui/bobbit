# cri.py

import random

# Metadata

NAME = 'cri'
ENABLE = True
PATTERN = r'^![Cc]ri\s*(?P<text>.*)$'
USAGE = '''Usage: ![Cc]ri
Displays a crying lenny face :,(
'''

CRYING = [
    ' ಥʖ̯ಥ ',
    ' (ಥ _ʖಥ) ',
    ' (TдT) ',
    ' (ಥ﹏ಥ) ',
    '（πーπ）',
    ' (Ｔ▽Ｔ) ',
    '（ｉДｉ）',
    ' ╰(ɵ̥̥ ˑ̫ ɵ̥̥ ╰) ',
    ' (≖͞_≖̥) ',
    ' ͡ಥ ͜ʖ ͡ಥ ',
    ' ( •́ ʖ̯ •̩̥̀ ) ',
    '（；へ：）',
    ':\'(',
    ' ;_; ',
    ' =\'( ',
    ' T^T ',
    ' ;-; '
]

# Command

async def cri(bot, message, text=None):
    response = random.choice(CRYING)
    if text:
        response += ' ' + text
    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, cri),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
# vaporwave.py

# Metdata

NAME    = 'vapor'
ENABLE  = True
PATTERN = r'^!vapor (?P<phrase>.*)'
USAGE   = '''Usage: !vapor <phrase>
Given a phrase, this transforms it into a vaporwave a e s t h e t i c phrase
with full-width characters. 
Example:
    > !vapor it works!
    ｉ ｔ   ｗ ｏ ｒ ｋ ｓ ！
'''

# Command

# Note - thanks to https://github.com/jonesmartins/vapyrwave for figuring out
# how to do full width :)

def transform_vaporwave(sentence):
    new_sentence = ''
    char_distance = ord('Ａ') - ord('A')  # 65248
    for character in sentence:
        ord_char = ord(character)
        if ord('!') <= ord_char <= ord('~'):
            character = chr(ord_char + char_distance)
        new_sentence += character

    return new_sentence

def make_horizontal(sentence, spaces=1):
    spaces_str = ' ' * spaces
    new_sentence = spaces_str.join([s for s in sentence])
    return new_sentence

async def vapor(bot, message, phrase):
    phrase   = phrase.lower().rstrip()
    response = make_horizontal(
        transform_vaporwave(phrase)
    )

    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, vapor),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

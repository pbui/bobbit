# imgr.py

import random
import re

import tornado.gen
import tornado.httpclient

# Metadata

NAME    = 'imgur'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!imgur\s*(?P<album>.*)'
USAGE   = '''Usage: !imgur <album>
Given an album, this module responds with an image from that Imgur album
Example:
    > !imgur sad
'''

# Constants

IMGUR_ALBUMS  = {
    'nope'          : 'http://imgur.com/a/JNzjB',
    'abandon'       : 'http://imgur.com/a/aYJkp',
    'disgust'       : 'http://imgur.com/a/AXues',
    'excited'       : 'http://imgur.com/a/1GOKT',
    'clapping'      : 'http://imgur.com/a/NzuZS',
    'stfu'          : 'http://imgur.com/a/FGIfa',
    'sad'           : 'http://imgur.com/a/qfkyX',
    'notbad'        : 'http://imgur.com/a/LoNV2',
    'popcorn'       : 'http://imgur.com/a/LPRbU',
    'haters'        : 'http://imgur.com/a/yGacg',
    'didntread'     : 'http://imgur.com/a/tVg8K',
    'mindblown'     : 'http://imgur.com/a/FEnwc',
    'upvotes'       : 'http://imgur.com/a/fG58m',
    'controversial' : 'http://imgur.com/a/A3Zqw',
    'downvotes'     : 'http://imgur.com/a/ixZeK',
    'confused'      : 'http://imgur.com/a/ywmyw',
    'coolstorybro'  : 'http://imgur.com/a/yIdY2',
    'dancing'       : 'http://imgur.com/a/wy22z',
    'umad'          : 'http://imgur.com/a/zKaIL',
    'dealwithit'    : 'http://imgur.com/a/K21Ft',
    'nofucks'       : 'http://imgur.com/a/cB34U',
    'fapping'       : 'http://imgur.com/a/QBTWF',
    'laughing'      : 'http://imgur.com/a/s16Zv',
    'self-inflicted': 'http://imgur.com/a/VvMv5',
    'animals'       : 'http://imgur.com/a/EGae0',
    'swag'          : 'http://imgur.com/a/ijrTZ',
    'slap'          : 'http://imgur.com/a/yCNp0',
    'racist'        : 'http://imgur.com/a/D87EB',
    'feels'         : 'http://imgur.com/a/SL6aO',
    'skill'         : 'http://imgur.com/a/S3TNe',
    'thanksobama'   : 'http://imgur.com/a/xGeus',
}

BAD_RESPONSES = (
    'Nope',
    'No results',
    'Nada',
    'Sorry',
    'Bzzt',
)

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, album=None):
    if album not in IMGUR_ALBUMS:
        bot.send_response(random.choice(BAD_RESPONSES), nick, channel)
        return

    url      = IMGUR_ALBUMS[album]
    client   = tornado.httpclient.AsyncHTTPClient()
    result   = yield tornado.gen.Task(client.fetch, url)
    text     = result.body.decode()
    images   = re.findall('<div id="([^"]+)" class="post">', text)
    response = None

    if images:
        response = u'http://i.imgur.com/{}.gif'.format(random.choice(images))

    if not response:
        try:
            images   = re.findall('meta property="og:image"\s+content="(http://i\.[^"?]+)"', text)
            response = random.choice(images)
        except IndexError:
            pass

    if not response:
        try:
            images   =  re.findall("gifUrl:.*//(i.imgur.com/.*.gif)'", text)
            response = 'http://{}'.format(random.choice(images))
        except IndexError:
            pass

    if not result:
        response = random.choice(BAD_RESPONSES)

    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

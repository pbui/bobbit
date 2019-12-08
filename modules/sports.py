import re

import tornado.gen
import tornado.httpclient

# Metadata

NAME    = 'sports'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!(?P<sport>nba|nfl|mlb|wnba|nhl|cfb)$'
USAGE   = '''Usage: ![nhl|nba|wnba|mlb|nfl|cfb]
Given a search query, this returns the first result from Google
Example:
    > !nba
    76ers 114 Celtics 75
'''

# Constants

ESPN_TEMPLATE = 'http://www.espn.com/{sport}/bottomline/scores'
SPORTS_ALIAS  = {
    'cfb': 'ncf',
}

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, sport):
    sport    = SPORTS_ALIAS.get(sport, sport)
    url      = ESPN_TEMPLATE.format(sport=sport)
    client   = tornado.httpclient.AsyncHTTPClient()
    result   = yield tornado.gen.Task(client.fetch, url)
    response = 'No results'

    try:
        text     = result.body.decode("UTF-8")\
                    .replace('%20', ' ')\
                    .replace('^', '')\
                    .replace('&', '\n')
        pattern  = re.compile(r"{}_s_left\d+=(.*)".format(sport))
        response = [match for match in re.findall(pattern, text) if ' ' in match]
    except (IndexError, ValueError) as e:
        bot.logger.warn(e)

    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

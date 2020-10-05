import re

# Metadata

NAME    = 'sports'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!(?P<sport>nba|nfl|mlb|wnba|nhl|cfb) ?(?P<team>.*)?$'
USAGE   = '''Usage: ![nhl|nba|wnba|mlb|nfl|cfb] <team_name>
Given a search query, this returns the scores from ESPN for the given sport or team
Example:
    > !nba
    76ers 114 Celtics 75
    Wizards 99 Warriors 88
    > !nba 76ers
    76ers 114 Celtics 75
'''

# Constants

ESPN_TEMPLATE = 'http://www.espn.com/{sport}/bottomline/scores'
SPORTS_ALIAS  = {
    'cfb': 'ncf',
}

# Command

async def command(bot, message, sport, team=None):
    sport    = SPORTS_ALIAS.get(sport, sport)
    url      = ESPN_TEMPLATE.format(sport=sport)
    response = 'No results'

    async with bot.http_client.get(url) as result:
        try:
            body = await result.text('UTF-8') # decode ClientResponse body
            text     = body.replace('%20', ' ')\
                        .replace('^', '')\
                        .replace('&', '\n')
            pattern  = re.compile(r"{}_s_left\d+=(.*)".format(sport))
            response = [match for match in re.findall(pattern, text) if ' ' in match]
            # filter results
            if team:
                team = team.title()
                response = [x for x in response if team in x]
            # return last 5 results
            response = 'No results' if not response else '\n'.join(response[-5:])
        except (IndexError, ValueError) as e:
            bot.logger.warn(e)

    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

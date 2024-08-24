import itertools
import logging
import re

# Metadata

NAME    = 'sports'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!(?P<sport>nba|nfl|mlb|cfb) ?(?P<team>.*)?$'
USAGE   = '''Usage: ![nba|mlb|nfl|cfb] <team_name>
Given a search query, this returns the scores from CBS Sports for the given
sport or team.
Example:
    > !nba
    76ers 114 Celtics 75
    Wizards 99 Warriors 88
    > !nba 76ers
    76ers 114 Celtics 75
'''

# Constants

URL_TEMPLATE = 'http://www.cbssports.com/{sport}/scoreboard'
TEAM_RX      = r'class="team-name-link">([^<]+)</a>.*?"total">([0-9]+)</td>'
SPORTS_ALIAS = {
    'cfb': 'college-football',
}

# Functions

def format_game(team_a, team_b):
    name_a, score_a = team_a
    name_b, score_b = team_b

    if int(score_a) > int(score_b):
        return f'{{bold}}{name_a:14}{{bold}} {{color}}{{green}}{score_a:>2}{{color}} - {name_b:14} {{color}}{{red}}{score_b:>2}{{color}}'
    elif int(score_a) < int(score_b):
        return f'{name_a:14} {{color}}{{red}}{score_a:>2}{{color}} - {{bold}}{name_b:14}{{bold}} {{color}}{{green}}{score_b:>2}{{color}}'
    else:
        return f'{name_a:14} {{color}}{{yellow}}{score_a:>2}{{color}} - {name_b:14} {{color}}{{yellow}}{score_b:>2}{{color}}'

# Command

async def command(bot, message, sport, team=None):
    sport = SPORTS_ALIAS.get(sport, sport)
    url   = URL_TEMPLATE.format(sport=sport)

    async with bot.http_client.get(url) as result:
        try:
            body  = await result.text()
            teams = re.findall(TEAM_RX, body)
            games = [
                bot.client.format_text(format_game(team_a, team_b))
                for team_a, team_b in itertools.batched(teams, 2)
                if team is None
                or team.lower() in team_a[0].lower()
                or team.lower() in team_b[0].lower()
            ]
        except (IndexError, ValueError) as e:
            logging.warn(e)

    if not games:
        games = ['No results']

    return [message.with_body(x) for x in games[:5]]

# Register

def register(bot):
    return (
        ('command', PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

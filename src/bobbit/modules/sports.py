import logging
import re

# Metadata

NAME    = 'sports'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!(?P<sport>cfb|mlb|nba|nfl|nhl|wnba) ?(?P<team>.*)?$'
USAGE   = '''Usage: ![cfb|mlb|nba|nfl|nhl|wnba] <team_name>
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
GAME_RX      = r'<div id="game-.*?</div></div></div>'
TEAM_RX      = r'class="team-name-link">([^<]+)</a>.*?"total">([0-9]+)</td>'
STATUS_RX    = r'<div class="game-status [^"]+"><div[^>]*>([^<]+)</div>'
SPORTS_ALIAS = {
    'cfb': 'college-football',
}

# Functions

def parse_games(text):
    for game_text in re.findall(GAME_RX, text):
        teams  = re.findall(TEAM_RX, game_text)
        status = re.findall(STATUS_RX, game_text)

        if not teams or not status:
            continue

        yield {
            'team_a': teams[0][0], 'score_a': int(teams[0][1]),
            'team_b': teams[1][0], 'score_b': int(teams[1][1]),
            'status': status[0]
        }

def format_game(game):
    team_a  = game['team_a']
    team_b  = game['team_b']
    score_a = game['score_a']
    score_b = game['score_b']
    status  = game['status']

    if score_a > score_b:
        text_a = f'{{bold}}{team_a:14}{{bold}} {{color}}{{green}}{score_a:>2}{{color}}'
        text_b = f'{team_b:14} {{color}}{{red}}{score_b:>2}{{color}}'
    elif score_a < score_b:
        text_a = f'{team_a:14} {{color}}{{red}}{score_a:>2}{{color}}'
        text_b = f'{{bold}}{team_b:14}{{bold}} {{color}}{{green}}{score_b:>2}{{color}}'
    else:
        text_a = f'{team_a:14} {{color}}{{yellow}}{score_a:>2}{{color}}'
        text_b = f'{team_b:14} {{color}}{{yellow}}{score_b:>2}{{color}}'

    if status == 'final':
        text_status = f'{{bold}}{status}{{bold}}'
    else:
        text_status = f'{{italic}}{status}{{italic}}'

    return f'{text_a} - {text_b} ({text_status})'

# Command

async def command(bot, message, sport, team=None):
    sport = SPORTS_ALIAS.get(sport, sport)
    url   = URL_TEMPLATE.format(sport=sport)

    async with bot.http_client.get(url) as result:
        try:
            body  = await result.text()
            games = [
                bot.client.format_text(format_game(game))
                for game in parse_games(body)
                if team is None
                or team.lower() in game['team_a'].lower()
                or team.lower() in game['team_b'].lower()
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

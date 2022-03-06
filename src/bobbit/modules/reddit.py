# reddit.py

import re

from bobbit.utils import shorten_url

# Metadata

NAME    = 'reddit'
ENABLE  = True
PATTERN = r'^!reddit (?P<subreddit>[^\s]*)\s*(?P<query>.*)$'
USAGE   = '''Usage: !reddit <subreddit> [<query>]
Given a subreddit, this returns an article from the subreddit that match the
query.
Example:
    > !reddit linuxmasterrace
'''

TITLE_PATTERN = r'(?P<url>[^\s]*reddit.com/[^\s]+)'

# Constants

REDDIT_TEMPLATE = 'http://reddit.com/r/{subreddit}/.json'

# Command

async def reddit(bot, message, subreddit, query=''):
    url = REDDIT_TEMPLATE.format(subreddit=subreddit)
    async with bot.http_client.get(url) as response:
        query     = query.lower()
        json_data = await response.json()
        response  = 'No results'

        try:
            for child in json_data['data']['children']:
                data  = child['data']
                title = data['title']
                url   = data['url']
                nsfw  = ' [NSFW]' if data['over_18'] else ''

                if query not in title.lower() and query not in url.lower():
                    continue

                if data['stickied']:
                    continue

                shorturl = await shorten_url(bot.http_client, url)
                response = bot.client.format_text(
                    '{color}{green}r/{}{color}: ' +
                    '{bold}{}{bold}{color}{red}{}{color} @ ' +
                    '{color}{blue}{}{color}',
                    subreddit, title, nsfw, shorturl
                )

                break
        except (IndexError, KeyError, ValueError):
            pass

        return message.with_body(response)

# Title Command

async def reddit_title(bot, message, url):
    async with bot.http_client.get(url) as response:
        try:
            text  = await response.text()
            title = re.findall(r'"title":"([^"]+)"}}}', text)[0]

            title, subreddit = title.rsplit(' : ', 1)
            return message.with_body(bot.client.format_text(
                '{color}{green}r/{}{color}: {bold}{}{bold}',
                subreddit, title
            ))
        except IndexError:
            pass

# Register

def register(bot):
    return (
        ('command', PATTERN      , reddit),
        ('command', TITLE_PATTERN, reddit_title),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

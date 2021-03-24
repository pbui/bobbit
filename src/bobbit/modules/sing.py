# sing.py

from bobbit.utils import parse_options

import requests
import re
import random

# Metadata

NAME    = 'sing'
ENABLE  = True
PATTERN = '^![Ss]ing (?P<query>.*$)'
USAGE   = '''Usage: !sing <title>
Given a song title and an optional artist, this module responds with a few lines from
the song.

Example:
    > !sing Truth Hurts
    Why're men great 'til they gotta be great?
'''

# Command

async def sing(bot, message, query):
    url         = 'https://search.azlyrics.com/search.php?q='
    query       = "+".join(query.rstrip().split())
    url_query   = url + query
    response    = requests.get(url_query).text
    result_re   = '1\. <a href=\"(.*)\"><b>\"(.*)\"</b>'

    # first search result
    re_search = re.search(result_re, response)

    if re_search:
        song_url    = re_search[1]
        song_title  = re_search[2]
        song_res    = requests.get(song_url).text.splitlines()

        # get lyrics
        for idx, line in enumerate(song_res):
            if line.endswith("Sorry about that. -->"):
                start_idx = idx + 1
            elif line.endswith("banner -->"):
                end_idx = idx - 5

        lyrics = song_res[start_idx:end_idx]

        # remove <br>
        lyrics = [lyric[:-4] for lyric in lyrics if lyric.endswith("<br>") and len(lyric) > 4]
        output = random.choice(lyrics)
    else:
        output = "No search results found."

    return message.with_body(output)


# Register

def register(bot):
    return (
        ('command', PATTERN, sing),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

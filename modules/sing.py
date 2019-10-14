#sing.py

from modules.__common__ import shorten_url

from urllib.parse import urlencode, unquote

import re, random, sys

import tornado.gen
import tornado.httpclient

from lxml import etree, html

#Metadata
NAME    = 'sing'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!sing (?P<query>.*$)'
USAGE   = '''Usage: !sing <song> [- <artist>]
Given a song title and an optional artist, this module responds with a few lines from 
the song.
Example:
    > !sing Truth Hurts
    Why're men great 'til they gotta be great?
'''

LYRICS_URL  = 'http://search.azlyrics.com/'

def parse_query(query):
    if " - " in query:
        query = query.split("-")
        title = query[0].strip()
        artist = query[1].strip()
    else:
        title = query.strip()
        artist = None

    return (title, artist)

def find_match(artist, title, results):
    for song in results:
        url = song[0][0].attrib['href']
        a_match = "".join(song[0][1].text[:])
        t_match = "".join(song[0][0][0].text[:])
        if artist.strip().lower() in a_match.strip().lower():
            if title.strip().lower() in t_match.strip().lower():
                return url
    return ""


def get_song_url(tree, title, artist):

    try:
        results = tree[1][3][0][0][-2][1][:]
    except:
        return "Song not found"

    if artist:
        try:
            song_url = find_match(artist, title, results)
        except:
            song_url = find_match(artist, title, results[1:-1])
    else: 
        try:
            song_url = results[0][0][0].attrib['href']
        except:
            song_url = results[1][0][0].attrib['href']

    if song_url == "":
        return "Song not found" 
    else: 
        return song_url
    
def get_lyrics(tree):
    results = tree[1][6][0][2][:]

    for i, r in enumerate(results):
    
        string = ""
        for each in r[1:]:
            string += etree.tostring(each, method="text", encoding="utf-8").decode("utf-8")
            
        lyrics = string.splitlines()
        lyrics = [x for x in lyrics if x != '']
        lyrics = [x for x in lyrics if not x.startswith("[")]

        if len(lyrics) > 1:
            i = random.randint(0, len(lyrics))
            return lyrics[i] +  " \\\\ " + lyrics[i+1]

    return "Lyrics not found"


# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, query=None):

    title, artist = parse_query(query)

    params  = {'q': query}
    url     = LYRICS_URL + '?' + urlencode(params)

    client  = tornado.httpclient.AsyncHTTPClient(defaults=dict(request_timeout=180, connect_timeout=60))
    result  = yield tornado.gen.Task(client.fetch, url)
    tree = etree.HTML(result.body)

    response = get_song_url(tree, title, artist)

    if response != "Song not found":
        song_url = response

        client  = tornado.httpclient.AsyncHTTPClient(defaults=dict(request_timeout=180, connect_timeout=60))
        result  = yield tornado.gen.Task(client.fetch, song_url)
        tree = etree.HTML(result.body)

        response = get_lyrics(tree)
   
    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

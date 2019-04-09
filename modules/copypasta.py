#!/usr/bin/env python3

# copypasta.py
# module for bobbit that pulls posts from r/copypasta
# i don't claim any responsibility for the content of the posts
# Gavin Inglis

import os
import requests
import random
import re
import tornado.gen
import tornado.httpclient
import json

# Metadata

NAME    = 'copypasta'
ENABLE  = True
TYPE    = 'command'
PATTERN = re.compile('^!copypasta$')
URL = 'https://www.reddit.com/r/copypasta/.json'

USAGE   = '''Usage: !copypasta
Displays a random post from r/copypasta\n
WARNING: can be pretty offcolor. Use at your own discretion
'''
# Functions

# def get_pasta(url=URL):
# 	# trick reddit w user agent
# 	headers  = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-20289-sp19'))}

# 	client = tornado.httpclient.AsyncHTTPClient()
# 	result = yield tornado.gen.Task(client.fetch, url)
# 	for r in json.loads(result.body.decode())['data']['children']:
# 		print(r)

# 	pastas = []
# 	for i in range(len(r)):
# 		# ignore empty result
# 		if len(r[i]['data']['selftext']) == 0:
# 			continue
# 		pastas.append(r[i]['data']['selftext'])
# 		#print(r[i]['data']['selftext'])

# 	response = random.choice(pastas)

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, url=URL):
    client = tornado.httpclient.AsyncHTTPClient()
    result = yield tornado.gen.Task(client.fetch, url)

    pastas = []
    try:
        for result in json.loads(result.body.decode())['data']['children']:
            data  = result['data']
            pasta = data['selftext']

            pastas.append(pasta)

    except (IndexError, KeyError, ValueError) as e:
        bot.logger.warn(e)
        response = 'No results'

    bot.send_response(random.choice(pastas), None if channel else nick, channel)

# Register

def register(bot):
    bot.suppress_taunts = set()
    return (
        (PATTERN, command),
    )
# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

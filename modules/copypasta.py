#!/usr/bin/env python3

# copypasta.py
# module for bobbit that pulls posts from r/copypasta
# i don't claim any responsibility for the content of the posts
# Gavin Inglis

import os
import requests
import random
import re

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

def get_pasta(url=URL):
	''' Load reddit data from specified URL into dictionary '''
	# trick reddit w user agent
	headers  = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-20289-sp19'))}
	response = requests.get(url, headers=headers)
	data = response.json()

	pastas = []
	for i in range(0,len(data['data']['children'])):
		# ignore empty result
		if len(data['data']['children'][i]['data']['selftext']) == 0:
			continue
		pastas.append(data['data']['children'][i]['data']['selftext'])

	return random.choice(pastas)

def command(bot, nick, message, channel, URL):
    response = get_pasta(URL)
    if response and not channel in bot.suppress_taunts:
        bot.send_message(response, None if channel else nick, channel)

# Register

def register(bot):
    bot.suppress_taunts = set()
    return (
        (PATTERN, command),
    )
# res = get_pasta(URL)
# print(res)
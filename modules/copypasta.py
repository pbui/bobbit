#!/usr/bin/env python3

# reddit.py
# gets info abt subreddits
# Gavin Inglis
# 2 20 2019

import os
import requests
import random

# Functions
URL = 'https://www.reddit.com/r/copypasta/.json'

def get_pasta(url=URL):
	''' Load reddit data from specified URL into dictionary '''
	# trick reddit w user agent
	headers  = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-20289-sp19'))}
	response = requests.get(url, headers=headers)
	data = response.json()

	text = []
	for i in range(0,len(data['data']['children'])):
		# get relevent info from data
		if len(data['data']['children'][i]['data']['selftext']) == 0:
			continue
		text.append(data['data']['children'][i]['data']['selftext'])

	return random.choice(text)

# Main Execution
result = get_pasta(URL)
print(result)
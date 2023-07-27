''' bobbit.protocol.slack '''

import itertools
import json
import logging
import re

import aiohttp

from bobbit.message       import Message
from bobbit.protocol.base import BaseClient

# Slack Constants

SLACK_API_DOMAIN = 'https://api.slack.com'
SLACK_CHANNEL_RX = r'<#[0-9A-Z]+\|([^>]+)>'

# Slack Client

class SlackClient(BaseClient):

    def __init__(self, *args, **kwargs):
        self.nick        = kwargs['nick']
        self.token       = kwargs['password']
        self.url         = None
        self.counter     = itertools.count()
        self.channels    = {}
        self.http_client = aiohttp.ClientSession()
        self.ws          = None

    # Slack methods

    async def get_channel(self, channel):
        if channel not in self.channels:
            url    = f'{SLACK_API_DOMAIN}/api/conversations.list'
            params = {
                'limit'           : 1000,
                'types'           : 'public_channel,private_channel',
                'exclude_archived': 'true',
                'exclude_members' : 'true',
                'token'           : self.token,
            }
            async with self.http_client.get(url, params=params) as response:
                data = await response.json()

            if data['ok']:
                for c in data['channels']:
                    self.channels['#' + c['name']] = c['id']

        try:
            return self.channels[channel]
        except KeyError:
            return channel

    # Client methods

    async def connect(self):
        ''' Connect to Slack via Websocket '''
        url    = f'{SLACK_API_DOMAIN}/api/rtm.connect'
        params = {'token': self.token}

        logging.info('Retrieving websocket URL from: %s', url)
        async with self.http_client.get(url, params=params) as response:
            data = await response.json()

        self.url = data['url']

        logging.info('Connecting to websocket: %s', self.url)
        self.ws  = await self.http_client.ws_connect(self.url)

    async def send_message(self, message):
        if message.channel.startswith('#'):
            message.channel = await self.get_channel(message.channel)

        message.body = self.format_message(message)

        await self.ws.send_str(json.dumps({
            'id'        : next(self.counter),
            'type'      : 'message',
            'channel'   : message.channel,
            'text'      : message.body,
        }))

        logging.debug('Sent message: %s', message)

    async def recv_message(self):
        message = None
        while not message:
            ws_message   = await self.ws.receive()
            json_message = json.loads(ws_message.data)
            logging.debug('Received JSON: %s', json_message)

            if json_message.get('type') != 'message':
                continue

            try:
                message = Message(
                    body    = re.sub(SLACK_CHANNEL_RX, r'#\1', json_message['text']),
                    nick    = json_message['user'],
                    channel = json_message['channel'],
                )
            except KeyError:
                pass

        logging.debug('Received message: %s', message)
        return message

    # Formatting

    @staticmethod
    def format_message(message):
        if message.highlighted:
            if message.nick.startswith('@') or message.nick.startswith('<'):
                return f'{message.nick}: {message.body}'
            else:
                return f'<@{message.nick}>: {message.body}'
        else:
            return message.body

    @staticmethod
    def format_text(text, *args, **kwargs):
        FORMAT_CODES = {
            'bold'       : '*',
            'B'          : '*',
            'color'      : '',
            'C'          : '',
            'italic'     : '_',
            'I'          : '_',
            'black'      : '',
            'blue'       : '',
            'green'      : '',
            'red'        : '',
            'brown'      : '',
            'magenta'    : '',
            'orange'     : '',
            'yellow'     : '',
            'lightgreen' : '',
            'cyan'       : '',
            'lightcyan'  : '',
            'lightblue'  : '',
            'pink'       : '',
            'gray'       : '',
            'lightgray'  : '',
            'default'    : '',
        }
        kwargs.update(FORMAT_CODES)
        return text.format(*args, **kwargs)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

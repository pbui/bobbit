''' bobbit.protocol.irc '''

import asyncio
import logging
import re

from bobbit.message       import Message
from bobbit.protocol.base import BaseClient

# IRC Constants

CRNL = b'\r\n'

PING_RE       = re.compile(r'^PING (?P<payload>.*)')
CHANMSG_RE    = re.compile(r':(?P<nick>.*?)!\S+\s+?PRIVMSG\s+(?P<channel>#+[-\w]+)\s+:(?P<body>[^\n\r]+)')
PRIVMSG_RE    = re.compile(r':(?P<nick>.*?)!\S+\s+?PRIVMSG\s+[^#][^:]+:(?P<body>[^\n\r]+)')
ERROR_RE      = re.compile(r'^ERROR :(?P<reason>.*?):.*')
MOTD_RE       = re.compile(r':(?P<server>.*?)\s+(?:376|422)')
REGISTERED_RE = re.compile(r':NickServ!.*NOTICE.*:.*(identified|logged in|accepted).*')

# IRC Client

class IRCClient(BaseClient):
    ''' Basic IRC Client

    Protocol References:

    - https://modern.ircdocs.horse/
    '''

    def __init__(self, nick, password, host=None, port=None, ssl=False, channels=None, colorize=True):
        # Account information
        self.nick     = nick
        self.password = password

        # Server information
        self.host     = host or 'irc.freenode.net'
        self.port     = port or '6667'
        self.ssl      = ssl
        self.channels = channels or []

        if not colorize:
            self.format_text = BaseClient.format_text

        # TCP Streams
        self.reader   = None
        self.writer   = None

        # IRC handlers
        self.handlers = [
            (CHANMSG_RE   , self._handle_channel_message),
            (PRIVMSG_RE   , self._handle_private_message),
            (PING_RE      , self._handle_ping),
            (ERROR_RE     , self._handle_error),
            (MOTD_RE      , self._handle_motd),
            (REGISTERED_RE, self._handle_registration),
        ]

    # IRC handlers

    async def _handle_channel_message(self, nick, channel, body):
        logging.debug('Handling Channel Message: %s, %s, %s', nick, channel, body)
        return Message(body, nick, channel)

    async def _handle_private_message(self, nick, body):
        logging.debug('Handling Private Message: %s, %s', nick, body)
        return Message(body, nick)

    async def _handle_error(self, reason):
        logging.debug('Handling Error: %s', reason)
        raise Exception('Disconnected') # TODO: Use custom exception

    async def _handle_ping(self, payload):
        logging.debug('Handling Ping: %s', payload)
        await self.send_message(f'PONG {payload}')

    async def _handle_motd(self, server):
        logging.debug('Handling MOTD')

        if self.password.startswith('oauth:'):  # Note: Twitch doesn't do registration
            await self._handle_registration()
        else:
            await self.send_message(Message(
                nick    = 'NickServ',
                channel = None,
                body    = f'IDENTIFY {self.password}',
            ))

    async def _handle_registration(self):
        logging.debug('Handling Registration')
        for channel in self.channels:
            await self.send_message(f'JOIN {channel}')

        await self.send_message(f'MODE {self.nick} +b')

    # Client methods

    async def connect(self):
        ''' Connect to IRC server and register '''
        self.reader, self.writer = await asyncio.open_connection(
            self.host, self.port, ssl=self.ssl
        )

        logging.info('Connected to %s:%s', self.host, self.port)

        # TODO: Add for SASL
        # NOTE: PASS works for freenode, snoonet, and soon ndlug
        if self.password.startswith('oauth:'):  # Twitch
            await self.send_message(f'PASS {self.password}')
        else:
            await self.send_message(f'PASS {self.nick}:{self.password}')
        await self.send_message(f'USER {self.nick} {self.host} bobbit :{self.nick}')
        await self.send_message(f'NICK {self.nick}')

    async def send_message(self, message):
        if isinstance(message, Message):
            message = self.format_message(message)

        self.writer.write(message.encode() + CRNL)
        logging.debug('Sent message: %s', message)
        await self.writer.drain()

    async def recv_message(self):
        message = None
        while not message:
            # Wait for non-empty line
            line = None
            while not line:
                line = (await self.reader.readline()).decode().rstrip()

            logging.debug('Received line: %s', line)

            # Check handlers
            for pattern, handler in self.handlers:
                arguments = pattern.match(line)
                if arguments:
                    message = await handler(**arguments.groupdict())

        logging.debug('Received message: %s', message)
        return message

    # Formatting

    @staticmethod
    def format_message(message):
        target  = message.channel if message.channel else message.nick
        command = 'NOTICE' if message.notice else 'PRIVMSG'
        if message.highlighted:
            return f'{command} {target} :\x02{message.nick}\x02: {message.body}'
        else:
            return f'{command} {target} :{message.body}'

    @staticmethod
    def format_text(text, *args, **kwargs):
        FORMAT_CODES = {
            'bold'       : '\x02',
            'B'          : '\x02',
            'color'      : '\x03',
            'C'          : '\x03',
            'black'      : '01',
            'blue'       : '02',
            'green'      : '03',
            'red'        : '04',
            'brown'      : '05',
            'magenta'    : '06',
            'orange'     : '07',
            'yellow'     : '08',
            'lightgreen' : '09',
            'cyan'       : '10',
            'lightcyan'  : '11',
            'lightblue'  : '12',
            'pink'       : '13',
            'gray'       : '14',
            'lightgray'  : '15',
            'default'    : '99',
        }
        kwargs.update(FORMAT_CODES)
        return text.format(*args, **kwargs)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

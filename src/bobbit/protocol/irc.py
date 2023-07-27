''' bobbit.protocol.irc '''

import asyncio
import logging
import re
import textwrap

from bobbit.message       import Message
from bobbit.protocol.base import BaseClient

# IRC Constants

CRNL = b'\r\n'

PING_RE       = re.compile(r'^PING (?P<payload>.*)')
CHANMSG_RE    = re.compile(r':(?P<nick>.*?)!\S+\s+?PRIVMSG\s+(?P<channel>#+[-\w]+)\s+:(?P<body>[^\n\r]+)')
PRIVMSG_RE    = re.compile(r':(?P<nick>.*?)!\S+\s+?PRIVMSG\s+[^#][^:]+:(?P<body>[^\n\r]+)')
ERROR_RE      = re.compile(r'^ERROR :(?P<reason>.*?):.*')
MOTD_RE       = re.compile(r':(?P<server>.*?)\s+(?:376|422)')
NAMES_RE      = re.compile(r':.*\s+(?:353)\s+[^\s]+\s+=\s+(?P<channel>#+[-\w]+)\s+:(?P<nicks>[^\n\r]+)')
JOIN_RE       = re.compile(r':(?P<nick>.*?)!\S+\s+?JOIN\s+(?P<channel>#+[-\w]+)')
PART_RE       = re.compile(r':(?P<nick>.*?)!\S+\s+?PART\s+(?P<channel>#+[-\w]+)')
QUIT_RE       = re.compile(r':(?P<nick>.*?)!\S+\s+?QUIT\s+:')
KICK_RE       = re.compile(r':.*!\S+\s+?KICK\s+(?P<channel>#+[-\w]+)\s+(?P<nick>[^\s]+)')
NICK_RE       = re.compile(r':(?P<old_nick>.*?)!\S+\s+?NICK\s+(?P<new_nick>[^\s]+)')
REGISTERED_RE = re.compile(r':NickServ!.*NOTICE.*:.*(identified|logged in|accepted).*')

MESSAGE_LENGTH_MAX = 512 - len(CRNL)

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
            (NAMES_RE     , self._handle_names),
            (JOIN_RE      , self._handle_join),
            (PART_RE      , self._handle_part),
            (QUIT_RE      , self._handle_quit),
            (KICK_RE      , self._handle_kick),
            (NICK_RE      , self._handle_nick),
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

    async def _handle_names(self, channel, nicks):
        return Message(f'@NAMES@ {nicks}', '@IRC@', channel)

    async def _handle_join(self, channel, nick):
        return Message(f'@JOIN@ {nick}', '@IRC@', channel)

    async def _handle_kick(self, channel, nick):
        return Message(f'@KICK@ {nick}', '@IRC@', channel)

    async def _handle_part(self, channel, nick):
        return Message(f'@PART@ {nick}', '@IRC@', channel)

    async def _handle_quit(self, nick):
        return Message(f'@QUIT@ {nick}', '@IRC@', None)

    async def _handle_nick(self, old_nick, new_nick):
        return Message(f'@NICK@ {old_nick} {new_nick}', '@IRC@', None)

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

        await self.send_message(f'MODE {self.nick} +B')

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

        if len(message) > MESSAGE_LENGTH_MAX:
            command, message = message.split(' :', 1)
            messages = [f'{command} :{m}' for m in textwrap.wrap(message, MESSAGE_LENGTH_MAX - len(command) - 2)]
        else:
            messages = [message]

        for message in messages:
            self.writer.write(message.encode() + CRNL)
            logging.debug('Sent message: %s', message)
            await self.writer.drain()

    async def recv_message(self):
        message = None
        while not message:
            line = (await self.reader.readline()).decode().rstrip()
            if not line:
                raise ConnectionResetError

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
        body    = message.body
        if message.highlighted:
            return f'{command} {target} :\x02{message.nick}\x02: {body}'
        else:
            return f'{command} {target} :{body}'

    @staticmethod
    def format_text(text, *args, **kwargs):
        FORMAT_CODES = {
            'bold'       : '\x02',
            'B'          : '\x02',
            'color'      : '\x03',
            'C'          : '\x03',
            'italic'     : '\x1D',
            'I'          : '\x1D',
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

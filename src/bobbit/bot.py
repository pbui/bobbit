''' bobbit.bot '''

import atexit
import asyncio
import logging

import yaml

from bobbit.config      import Configuration
from bobbit.history     import History
from bobbit.http_client import HTTPClient
from bobbit.message     import Message
from bobbit.modules     import load_modules

class Bobbit():

    def __init__(self, config_dir=None, log_path=None, debug=False, local=False):
        self.config      = Configuration(config_dir, log_path, debug, local)
        self.modules     = []
        self.commands    = []
        self.timers      = []
        self.history     = History()
        self.users       = self.load_users() or {}

        self.http_client = None
        self.client      = None
        self.outgoing    = None

        atexit.register(self.save_users)

    # Message processing

    async def _send_messages(self):
        while True:
            message = await self.outgoing.get()
            await self.client.send_message(message)
            self.outgoing.task_done()
            logging.debug('Sent message: %s', message)

    async def _recv_messages(self):
        while True:
            # Wait for message from client
            message = await self.client.recv_message()
            logging.debug('Received message: %s', message)

            # Check for matching commands
            async for responses in self.process_message(message):
                if not responses:
                    continue

                if isinstance(responses, (str, Message)):
                    responses = [responses]

                for response in responses:
                    if isinstance(response, str):
                        response = Message(response, message.nick, message.channel)

                    await self.outgoing.put(response)

            # Add message to history
            self.history.insert(message)

            # Update user last seen and channel
            self.update_user_seen(message.nick, message.timestamp)
            self.update_user_channel(message.nick, message.channel)

    async def process_message(self, message):
        ''' Process a single message '''
        for pattern, command in self.commands:
            arguments = pattern.match(message.body)
            if not arguments:
                continue

            logging.debug('Found match: %s', command)
            try:
                yield await command(self, message, **arguments.groupdict())
            except Exception as e:
                logging.exception(e)

    # Controls

    def reload(self):
        ''' Reload bot modules '''
        for timer in self.timers:
            timer.cancel()

        self.modules, self.commands, self.timers = load_modules(self, self.config.modules_dir)

    def restart(self):
        raise NotImplementedError

    # Users

    def load_users(self):
        users_path = self.config.get_config_path('users.yaml')
        try:
            logging.info('Loading users from %s', users_path)
            return yaml.safe_load(open(users_path))
        except (IOError, OSError) as e:
            logging.warning('Unable to load %s: %s', users_path, e)
            return {}

    def save_users(self):
        users_path = self.config.get_config_path('users.yaml')
        with open(users_path, 'w') as stream:
            logging.info('Saving users to %s', users_path)
            yaml.safe_dump(self.users, stream, default_flow_style=False)

    def update_user_seen(self, nick, timestamp):
        logging.debug('Updating last_seen for %s: %s', nick, timestamp)
        if nick not in self.users:
            self.users[nick] = {'last_seen': timestamp}
        else:
            self.users[nick]['last_seen'] = timestamp

    def update_user_channel(self, nick, channel):
        logging.debug('Updating channel for %s: %s', nick, channel)
        if nick not in self.users:
            self.users[nick] = {'channels': [channel]}
        elif 'channels' not in self.users[nick]:
            self.users[nick]['channels'] = [channel]
        elif channel not in self.users[nick]['channels']:
            self.users[nick]['channels'].append(channel)

    def remove_user_channel(self, nick, channel):
        logging.debug('Removing channel for %s: %s', nick, channel)
        try:
            self.users[nick]['channels'].remove(channel)
        except (KeyError, ValueError):
            pass

    async def _checkpoint_users(self):
        while True:
            await asyncio.sleep(5*60)
            try:
                self.save_users()
            except Exception as e:
                logging.exception(e)

    # Main execution

    async def run(self):
        # Load modules
        self.reload()

        # Start HTTP Client
        self.http_client = HTTPClient()

        # Start Protocol Client
        self.client = self.config.client(
            nick     = self.config.nick,
            password = self.config.password,
            host     = self.config.host,
            port     = self.config.port,
            ssl      = self.config.use_ssl,
            channels = self.config.channels,
            colorize = self.config.colorize,
        )
        try:
            await self.client.connect()
        except OSError as e:
            logging.exception(e)
            return 'Failed to connect'

        # Start background tasks
        self.outgoing = asyncio.Queue(maxsize=10)

        try:
            await asyncio.gather(
                self._send_messages(),
                self._recv_messages(),
                self._checkpoint_users(),
            )
        except Exception as e:
            logging.exception(e)
            self.http_client.close()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

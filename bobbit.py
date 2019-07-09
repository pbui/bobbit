#!/usr/bin/env python3

import functools
import getpass
import glob
import itertools
import json
import logging
import os
import re
import socket
import sys

from importlib import reload

import yaml

import tornado.gen
import tornado.ioloop
import tornado.options
import tornado.tcpclient
import tornado.websocket

# IRC Client

class IRCClient(object):
    ''' IRC Client '''

    # Regular Expressions

    PING_RE     = re.compile(r'^PING (?P<payload>.*)')
    CHANMSG_RE  = re.compile(r':(?P<nick>.*?)!\S+\s+?PRIVMSG\s+(?P<channel>#+[-\w]+)\s+:(?P<message>[^\n\r]+)')
    PRIVMSG_RE  = re.compile(r':(?P<nick>.*?)!\S+\s+?PRIVMSG\s+[^#][^:]+:(?P<message>[^\n\r]+)')
    REGISTER_RE = re.compile(r':(?P<server>.*?)\s+(?:376|422)')

    # Connect

    @tornado.gen.coroutine
    def connect(self):
        ''' Connect to IRC server, authorize, register, and identify '''
        self.logger.info('Connecting to %s:%d', self.host, self.port)

        # Check SSL
        if self.use_ssl:
            import ssl
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        else:
            self.ssl_context = None

        # Connect to IRC server
        self.tcp_client = tornado.tcpclient.TCPClient()
        self.tcp_stream = None
        while not self.tcp_stream:
            try:
                self.tcp_stream = yield self.tcp_client.connect(self.host, self.port, ssl_options=self.ssl_context)
                self.tcp_stream.set_close_callback(lambda: sys.exit(1))
            except socket.gaierror as e:
                self.tcp_stream = None

        # Send connection password (e.g. Twitch)
        if self.password.startswith('oauth:'):      # Twitch
            self.logger.info('Sending Connection Password: %s', self.password)
            self.send('PASS {}'.format(self.password))

        # Authorize
        self.logger.info('Authorizing as %s', self.nick)
        self.send('USER {} {} bobbit :{}'.format(self.nick, self.host, self.nick))

        # Register
        self.logger.info('Registering as %s', self.nick)
        self.send('NICK {}'.format(self.nick))

        if self.password.startswith('token:'):    # Mattermost
            token   = self.password.split(':')[-1]
            message = 'LOGIN {} token={}'.format(self.nick, token)
            self.logger.info('Logging in with Token: %s', token)
            self.send_command('PRIVMSG', message, 'mattermost', None)

        # Add handlers
        self.handlers   = [
            (self.PING_RE    , self.handle_ping),
            (self.CHANMSG_RE , self.handle_channel_message),
            (self.PRIVMSG_RE , self.handle_private_message),
            (self.REGISTER_RE, self.handle_registration),
        ]

        # Start reading
        self.recv_message(b'')

    # Send / Receive Messages

    @tornado.gen.coroutine
    def send(self, message):
        self.logger.debug('SEND: %s', message)
        message += '\r\n'
        yield self.tcp_stream.write(message.encode('utf-8'))

    def send_command(self, command, message, nick=None, channel=None):
        if channel:
            receiver = channel
        elif nick:
            receiver = nick
        else:
            receiver = None

        if receiver:
            self.send('{} {} :{}'.format(command, receiver, message))
        else:
            self.logger.warning('No channel or nick specified for: %s', message)

    def send_message(self, message, nick=None, channel=None):
        self.send_command('PRIVMSG', message, nick, channel)

    def send_notice(self, message, nick=None, channel=None):
        self.send_command('NOTICE', message, nick, channel)

    def recv_message(self, message):
        # Receive message
        message = message.decode().rstrip()
        self.logger.debug('RECV: %s', message)

        # Process handlers
        for pattern, callback in self.handlers:
            match = pattern.match(message)
            if match:
                try:
                    callback(**match.groupdict())
                except Exception as e:
                    self.logger.exception('Unhandled exception: %s', e)

        # Wait for next message
        self.tcp_stream.read_until(b'\n', self.recv_message)

    def format_response(self, response, nick=None, channel=None, prefix=False):
        return '{}{}: {}'.format(self.nick_prefix, nick, response) if prefix else response

    def format_bold(self, text):
        return '\x02{}\x02'.format(text)

    # Handlers

    def handle_ping(self, payload):
        self.logger.debug('Handling PING: %s', payload)
        self.send('PONG {}'.format(payload))

    def handle_registration(self, server):
        def complete_registration():
            # Join channels
            for channel in self.channels:
                self.logger.info('Joining %s', channel)
                self.send('JOIN {}'.format(channel))

        # Identify
        self.logger.info('Identifying as %s', self.nick)
        if not self.password.startswith('CONN:'):
            self.send_message('IDENTIFY {}'.format(self.password), nick='NickServ')

        # Declare as bot
        self.logger.info('Declaring as bot')
        self.send('MODE {} +B'.format(self.nick))

        # Delay joining channels to allow for identification
        tornado.ioloop.IOLoop.current().call_later(5.0, complete_registration)

# Slack Client

class SlackClient(object):
    API_DOMAIN = 'https://api.slack.com'

    @tornado.gen.coroutine
    def connect(self):
        self.channels = {}

        self.url = None
        http_uri = '{}/api/rtm.connect?token={}'.format(self.API_DOMAIN, self.token)
        self.logger.info('Retrieving websocket URL from: %s', http_uri)

        while not self.url:
            try:
                response = yield tornado.httpclient.AsyncHTTPClient().fetch(http_uri)
                data     = json.loads(response.body)
                if data['ok']:
                    self.url = data['url']
                    self.id  = data['self']['id']
            except socket.gaierror:
                continue

        self.logger.info('Connecting to websocket: %s', self.url)
        self.ws      = yield tornado.websocket.websocket_connect(self.url)
        self.counter = itertools.count()

        self.process_messages()

    @tornado.gen.coroutine
    def process_messages(self):
        while True:
            message = yield self.ws.read_message()
            self.logger.debug('RECV: %s', message)
            if message is None:
                break

            message = json.loads(message)
            try:
                if message['type'] == 'message':
                    self.handle_channel_message(message['user'], message['channel'], message['text'])
            except KeyError:
                pass

        self.connect()

    def send_notice(self, message, nick=None, channel=None):
        self.send_message(message, nick, channel)

    @tornado.gen.coroutine
    def send_message(self, message, nick=None, channel=None):
        if channel.startswith('#'):
            channel = yield self.get_channel(channel)

        try:
            self.ws.write_message(json.dumps({
                'id'        : next(self.counter),
                'type'      : 'message',
                'channel'   : channel,
                'text'      : message,
            }))
        except AttributeError:
            self.logger.info('Disconnect detected, exiting...')
            self.connect()
            self.send_message(message, nick, channel)

    def format_response(self, response, nick=None, channel=None, prefix=False):
        if prefix:
            if nick.startswith(self.nick_prefix) or nick.startswith('<'):
                return '{}: {}'.format(nick, response)
            else:
                return '<{}{}>: {}'.format(self.nick_prefix, nick, response)
        else:
            return response

    def format_bold(self, text):
        return '*{}*'.format(text)

    @tornado.gen.coroutine
    def get_channel(self, channel):
        if channel not in self.channels:
            http_uri = '{}/api/channels.list?exclude_archived=true&exclude_members=true&token={}'.format(self.API_DOMAIN, self.token)
            response = yield tornado.httpclient.AsyncHTTPClient().fetch(http_uri)
            data     = json.loads(response.body)
            if data['ok']:
                for c in data['channels']:
                    self.channels['#' + c['name']] = c['id']

        try:
            return self.channels[channel]
        except KeyError:
            return channel

# Bobbit

class Bobbit(object):

    def __init__(self, config_dir=None, **kwargs):
        self.logger      = logging.getLogger()
        self.modules     = {}
        self.commands    = []
        self.timers      = []

        self.load_configuration(config_dir)
        self.load_modules()

    # Modules

    def load_modules(self):
        self.logger.info('Importing modules from %s', self.modules_dir)

        # Keep track of modules, commands, and timers
        modules  = {}
        commands = []
        timers   = []

        # Shutdown old timers
        for timer in self.timers:
            timer.stop()
            del timer

        modules_root = os.path.dirname(self.modules_dir)
        if not modules_root in sys.path:
            sys.path.insert(modules_root, 0)

        # Iterate over modules in directory
        for module_path in glob.glob('{}/*.py'.format(self.modules_dir)):
            module_name = module_path.replace(modules_root + '/', '')
            module_name = module_name[:-3].replace('/', '.').replace('..', '')

            if '__' in module_name:
                continue

            # Load or re-load module
            try:
                self.logger.info('Loading %s', module_name)
                if module_name in self.modules:
                    module = self.modules[module_name]
                    reload(module)
                else:
                    module = __import__(module_name, globals(), locals(), -1)

                modules[module_name] = module
            except ImportError as e:
                self.logger.warning('Failed to import module %s: %s', module_name, e)
                continue

            # Enable module
            try:
                if module.TYPE == 'command' and module.ENABLE:
                    self.logger.info('Enabling %s command', module_name)
                    commands.extend(module.register(self))
                elif module.TYPE == 'timer' and module.ENABLE:
                    self.logger.info('Enabling %s timer', module_name)
                    for timeout, timer in module.register(self):
                        partial = functools.partial(timer, self)
                        timer   = tornado.ioloop.PeriodicCallback(partial, timeout*1000)
                        timer.start()
                        timers.append(timer)
            except Exception as e:
                self.logger.warning('Failed to enable module %s: %s', module_name, e)

        # Update instance modules and commands
        self.modules  = modules
        self.commands = [(re.compile(p), c) for p, c in commands]
        self.timers   = timers

    # Handlers

    def handle_channel_message(self, nick, channel, message):
        self.logger.debug('Handling Channel Message: %s | %s | %s', channel, nick, message)
        self.process_command(nick, message, channel)

    def handle_private_message(self, nick, message):
        self.logger.debug('Handling Private Message: %s | %s', nick, message)
        self.process_command(nick, message)

    def process_command(self, nick, message, channel=None):
        for pattern, callback in self.commands:
            match = pattern.match(message)
            if match:
                self.logger.debug('MATCHED: %s', pattern)
                callback(self, nick, message, channel, **match.groupdict())

    def send_response(self, response, nick=None, channel=None, notice=False):
        if response is None or (nick is None and channel is None):
            return

        try:
            prefix = nick.prefix
        except AttributeError:
            prefix = False

        if isinstance(response, str):
            if notice:
                self.send_notice(response, nick, channel)
            else:
                response = self.format_response(response, nick, channel, prefix)
                self.send_message(response, nick, channel)
        else:
            for r in response:
                self.send_response(r, nick, channel, notice)

    # Configuration

    def load_configuration(self, config_dir=None):
        ''' Load configuration from YAML file '''
        self.config_dir  = os.path.expanduser(config_dir or '~/.config/bobbit')
        self.config_path = os.path.join(self.config_dir, 'bobbit.yaml')
        self.modules_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules'))

        if os.path.exists(self.config_path):
            config = yaml.load(open(self.config_path))
        else:
            config = {}

        self.logger.info('Configuration Directory: %s', self.config_dir)
        self.logger.info('Configuration Path:      %s', self.config_path)
        self.logger.info('Modules Path:            %s', self.modules_dir)

        self.nick        = config.get('nick'       , 'bobbit')
        self.nick_prefix = config.get('nick_prefix', '')
        self.owners      = config.get('owners'     , [getpass.getuser()])
        self.use_ssl     = config.get('ssl'        , False)

        self.logger.info('Nick:           %s', self.nick)
        self.logger.info('Nick Prefix:    %s', self.nick_prefix)
        self.logger.info('Owners:         %s', ', '.join(self.owners))
        self.logger.info('SSL:            %s', self.use_ssl)

        if config.get('token', None):
            self.__class__  = type('SlackBobbit', (Bobbit, SlackClient), {})
            self.token       = config.get('token'   , '')
            self.logger.info('Token:          %s'   , self.token)
        else:
            self.__class__  = type('IRCBobbit', (Bobbit, IRCClient), {})
            self.host        = config.get('host'    , 'irc.freenode.net')
            self.port        = config.get('port'    , 6667)
            self.password    = config.get('password', '')
            self.channels    = config.get('channels', [])

            self.logger.info('Server:         %s:%d', self.host, self.port)
            self.logger.info('Password:       %s'   , self.password)
            self.logger.info('Channels:       %s'   , ', '.join(self.channels))

    # Run

    def run(self):
        self.connect()
        tornado.ioloop.IOLoop.current().start()

# Main Execution

if __name__ == '__main__':
    tornado.options.define('config_dir', default=None,  help='Configuration directory')
    tornado.options.parse_command_line()

    options = tornado.options.options.as_dict()
    bobbit  = Bobbit(**options)
    bobbit.run()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

# rpc.py

import os
import random
import shlex

import time
import tornado.process

# Metadata

NAME    = 'rpc'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!rpc (?P<arguments>.*)'
USAGE   = '''Usage: !rpc <arguments>

Executes a command and displays its results.  This is extremely dangerous, so
the generic RPC command is abstracted away behind specific commands.

Example:
    > !ping h4x0r.space

'''

# Constants

TIMEOUT = 5
DENIALS = (
    'Slow down',
    'Whoa there',
    'Not so fast',
    'EAGAIN',
    'haste, makes waste',
    '503',
)

# Generic Command

@tornado.gen.coroutine
def execute(bot, nick, message, channel, command, environ=None):
    if time.time() - bot.rpc_timestamp < 5:
        bot.send_response(random.choice(DENIALS), nick, channel)
        bot.rpc_timestamp = time.time()
        return

    command  = shlex.split(command) if isinstance(command, str) else command
    process  = tornado.process.Subprocess(command, stdout=tornado.process.Subprocess.STREAM, env=environ)
    response = yield tornado.gen.Task(process.stdout.read_until_close)
    bot.send_response(response.decode().splitlines(), nick, channel)
    bot.rpc_timestamp = time.time()

# Specific Commands

def ping(bot, nick, message, channel, host):
    command = ['ping', '-c', '3', '-w', '3', host]
    return execute(bot, nick, message, channel, command)

def figlet(bot, nick, message, channel, phrase):
    command = ['figlet', phrase]
    return execute(bot, nick, message, channel, command)

def cowsay(bot, nick, message, channel, phrase):
    command = ['cowsay', phrase]
    return execute(bot, nick, message, channel, command)

def mpc(bot, nick, message, channel, host, action):
    if hasattr(nick, 'prefix') or nick not in bot.owners:
        return

    command = ['ssh', '-t', 'cable', 'mpc', '--host=' + host, action]
    environ = dict(os.environ, **{'SSH_AUTH_SOCK': os.path.expanduser('~/.ssh/agent')})
    return execute(bot, nick, message, channel, command, environ)

# Register

def register(bot):
    bot.rpc_timestamp = time.time()
    return (
	('^!ping (?P<host>.*)', ping),
	('^!cowsay (?P<phrase>.*)', cowsay),
	('^!figlet (?P<phrase>.*)', figlet),
	('^!mpc (?P<host>.*) (?P<action>.*)', mpc),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:


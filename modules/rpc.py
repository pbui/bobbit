# rpc.py

import os
import shlex

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

# Generic Command

@tornado.gen.coroutine
def execute(bot, nick, message, channel, command, environ=None):
    command  = shlex.split(command) if isinstance(command, str) else command
    process  = tornado.process.Subprocess(command, stdout=tornado.process.Subprocess.STREAM, env=environ)
    response = yield tornado.gen.Task(process.stdout.read_until_close)
    bot.send_response(response.decode().splitlines(), nick, channel)

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
    if hasattr(nick, 'prefix') or nick != bot.owner:
        return

    command = ['ssh', '-t', 'cable', 'mpc', '--host=' + host, action]
    environ = dict(os.environ, **{'SSH_AUTH_SOCK': os.path.expanduser('~/.ssh/agent')})
    return execute(bot, nick, message, channel, command, environ)

# Register

def register(bot):
    return (
	('^!ping (?P<host>.*)', ping),
	('^!cowsay (?P<phrase>.*)', cowsay),
	('^!figlet (?P<phrase>.*)', figlet),
	('^!mpc (?P<host>.*) (?P<action>.*)', mpc),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:


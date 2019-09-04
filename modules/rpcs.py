# rpc.py

'''
# Configuration

Store RPCs in rpcs.yaml file in bobbit configuration directory:

    rpcs:
        ping:
            command:    'ping -c 3 -w 3 {argument0}'
        figlet:
            command:    'figlet {arguments}'
        mpc:
            command:    'ssh -t cable mpc --host={argument0} {argument1}'
            environ:
                SSH_AUTH_SOCK:    '/home/pbui/.ssh/agent'
            owners:     True
'''

import os
import random
import shlex
import time

import yaml
import tornado.process

# Metadata

NAME    = 'rpc'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!rpc (?P<program>[^ ]+)\s*(?P<arguments>.*)'
USAGE   = '''Usage: !rpc <program> <arguments>

Executes a command and displays its results.  This is extremely dangerous, so
the generic RPC command is abstracted away behind specific commands.

Example:
    > !rpc ping h4x0r.space

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

# Globals

RPCS = {}

# Command

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

@tornado.gen.coroutine
def command(bot, nick, message, channel, program=None, arguments=None):
    if program not in RPCS:
        return

    program   = RPCS[program]
    environ   = program.get('environ', {})
    args      = dict(enumerate(arguments.split()))
    command   = shlex.split(program.get('command', '').format(
        arguments = arguments,
        argument0 = args.get(0, ''),
        argument1 = args.get(1, ''),
        argument2 = args.get(2, ''),
        argument3 = args.get(3, ''),
    ))

    if program.get('owners', False) and (hasattr(nick, 'prefix') or nick not in bot.owners):
        return

    bot.logger.debug('RPC command: %s', command)
    yield execute(bot, nick, message, channel, command, environ)

# Register

def register(bot):
    global RPCS

    bot.rpc_timestamp = time.time()

    try:
        rpcs_path = os.path.join(bot.config_dir, 'rpcs.yaml')
        rpcs_data = yaml.safe_load(open(rpcs_path))
        RPCS      = rpcs_data.get('rpcs', {})
    except (KeyError, IOError):
        pass

    bot.logger.debug('RPCs: %s', RPCS)
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

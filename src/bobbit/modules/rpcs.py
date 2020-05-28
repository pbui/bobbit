# rpc.py

'''
# Configuration

Store RPCs in rpcs.yaml file in bobbit configuration directory:

    ping:
        command:    'ping -c 3 -w 3 {argument0}'
    figlet:
        command:    'figlet {arguments}'
        owners:     True
'''

import asyncio
import logging
import random
import shlex
import time

# Metadata

NAME    = 'rpc'
ENABLE  = True
PATTERN = r'^!rpc (?P<program>[^ ]+)\s*(?P<arguments>.*)'
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

RPCS          = {}
RPC_TIMESTAMP = None

# Command

async def execute(bot, message, command):
    global RPC_TIMESTAMP

    if time.time() - RPC_TIMESTAMP < 5:
        RPC_TIMESTAMP = time.time()
        return message.with_body(random.choice(DENIALS))

    command = shlex.split(command) if isinstance(command, str) else command
    process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE)

    stdout, _ = await process.communicate()
    await process.wait()
    RPC_TIMESTAMP  = time.time()
    return stdout.decode().splitlines()

async def rpc(bot, message, program=None, arguments=None):
    if program not in RPCS:
        return

    program   = RPCS[program]
    args      = dict(enumerate(arguments.split()))
    command   = shlex.split(program.get('command', '').format(
        arguments = arguments,
        argument0 = args.get(0, ''),
        argument1 = args.get(1, ''),
        argument2 = args.get(2, ''),
        argument3 = args.get(3, ''),
    ))

    # If owners is set, then only allow bot owners to run command
    if program.get('owners', False) and (message.highlighted or message.nick not in bot.config.owners):
        return

    logging.debug('RPC command: %s', command)
    return await execute(bot, message, command)

# Register

def register(bot):
    global RPCS, RPC_TIMESTAMP

    RPCS          = bot.config.load_module_config('rpcs')
    RPC_TIMESTAMP = time.time()

    logging.debug('RPCs: %s', RPCS)
    return (
        ('command', PATTERN, rpc),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

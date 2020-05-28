''' bobbit.modules '''

import asyncio
import glob
import importlib
import logging
import os
import re
import sys

# Timer factory

def Timer(bot, timeout, callback):
    ''' Timer task that periodically executes callback '''
    async def _timer(bot, timeout, callback):
        while True:
            await asyncio.sleep(timeout)
            try:
                await callback(bot)
            except Exception as e:
                logging.exception(e)

    return asyncio.create_task(_timer(bot, timeout, callback))


# Load modules functions

def load_modules(bot, modules_dir=None):
    ''' Load all modules from modules_dir.

    Note: caller must shutdown timers beforehand.
    '''
    modules_dir  = modules_dir or os.path.dirname(__file__)
    modules_root = os.path.dirname(modules_dir)

    logging.info('Loading modules from %s', modules_dir)

    # Keep track of modules, commands, and timers
    modules  = []
    commands = []
    timers   = []

    # Make sure modules root is in import path
    if not modules_root in sys.path:
        sys.path.insert(0, modules_root)

    # Iterate over modules in directory
    for module_path in glob.glob(f'{modules_dir}/*.py'):
        module_name = module_path.replace(modules_root + '/', '')
        module_name = module_name[:-3].replace('/', '.')

        if module_name.endswith('__'):
            continue

        module, module_commands, module_timers = load_module(bot, module_name)
        modules.append(module)
        commands.extend(module_commands)
        timers.extend(module_timers)

    return modules, commands, timers

def load_module(bot, module_name):
    ''' Load a single module '''
    commands = []
    timers   = []

    # Load or reload module
    logging.info('Loading %s', module_name)
    if module_name in sys.modules:
        module = importlib.reload(sys.modules[module_name])
    else:
        module = importlib.import_module(module_name)

    # Enable module
    if module.ENABLE:
        try:
            for kind, parameter, callback in module.register(bot):
                if kind == 'command':
                    logging.info('Enabling %s command', module_name)
                    commands.append((re.compile(parameter), callback))
                elif kind == 'timer':
                    logging.info('Enabling %s timer', module_name)
                    timers.append(Timer(bot, parameter, callback))
        except Exception as e:
            logging.warning('Failed to enable module %s: %s', module_name, e)

    return (module, commands, timers)

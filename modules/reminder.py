# reminder.py ---------------------------------------------------------------------

import shelve
import datetime
from pytz import timezone
from dateutil.parser import parse

import collections
import logging
import os
import yaml

import tornado.gen
import tornado.httpclient
import tornado.options
import tornado.process

# Metadata ---------------------------------------------------------------------

NAME     = 'reminder'
ENABLE   = True
TYPE     = {'timer', 'command'}
REMINDER_TEMPLATE = 'You asked me to remind you about "{content}" on {date}.'
RESPONSE_TEMPLATE = 'Sure, I will remind you on {time}.'
FAILURE_TEMPLATE = 'Sorry, I didn\'t quite understand that.'
USAGE   = '''Usage: !reminder <time> "<content>"
When the time comes, I will DM you to remind you about anything you ask.
Example:
    > !reminder on sunday "Do Systems homework"
    > !reminder 12/25 7AM "Merry Christmas!"
'''
PATTERN  = '^!reminder (?P<time>.*)"(?P<content>.*)"'
TIMEZONE = timezone('US/East-Indiana')

# Timer ------------------------------------------------------------------------

@tornado.gen.coroutine
def timer(bot):
    # Read reminders
    cache_path = os.path.join(bot.config_dir, 'reminder.cache')

    with shelve.open(cache_path, 'c') as reminder_cache:
        if 'reminders' not in reminder_cache:
            reminder_cache['reminders'] = []
        now       = datetime.datetime.now(TIMEZONE)
        past      = [entry for entry in reminder_cache['reminders'] if entry['reminder_time'] <= now]
        remaining = [entry for entry in reminder_cache['reminders'] if entry['reminder_time'] > now]
        reminder_cache['reminders'] = remaining
        for entry in past:
            message = REMINDER_TEMPLATE.format(content=entry['content'], date=entry['creation_time'].strftime("%B %d"))
            bot.send_message(message, nick=entry['nick'])
            bot.logger.info('Delivered reminder to %s', entry['nick'])

# Command ----------------------------------------------------------------------

def command(bot, nick, message, channel, time, content):
    cache_path = os.path.join(bot.config_dir, 'reminder.cache')
    try:
        now = datetime.datetime.now(TIMEZONE)
        reminder_time = parse(time, default=now)
        with shelve.open(cache_path, 'c') as reminder_cache:
            if reminder_cache['reminders'] is None:
                reminder_cache['reminders'] = []
            reminder = {'reminder_time': reminder_time, 'content': content, 'creation_time': now}
            reminder_cache['reminders'] = reminder_cache['reminders'] + [reminder]
        bot.send_response(RESPONSE_TEMPLATE.format(reminder_time.strftime("%b %d, %Y at %I:%M%p")), nick)
    except ValueError:
        bot.send_response(FAILURE_TEMPLATE, nick)

# Register ---------------------------------------------------------------------

def register(bot):
    config_path  = os.path.join(bot.config_dir, 'reminder.yaml')
    feeds_config = yaml.load(open(config_path))
    timeout      = feeds_config.get('timeout', 5*60)
    timer_info   = ((timeout, timer),)
    command_info = ((PATTERN, command),)
    return (command_info, timer_info)

# Main Execution ---------------------------------------------------------------

if __name__ == '__main__':
    tornado.options.define('config_dir', default=None,  help='Configuration directory')
    tornado.options.parse_command_line()
    options = tornado.options.options.as_dict()

    try:
        script(os.path.expanduser(options.get('config_dir', '~/.config/bobbit')))
    except Exception as e:
        logging.getLogger().warning(e)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: --------------------------------

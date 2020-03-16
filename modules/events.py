# events.py

import dbm.gnu
import collections
import json
import logging
import os
import re
import sys
import time

import icalendar
import datetime
import dateutil
import yaml

import tornado.gen
import tornado.httpclient
import tornado.options
import tornado.process

from modules.__common__ import shorten_url, strip_html

# Metadata

NAME     = 'events'
ENABLE   = True
TYPE     = 'timer'
TEMPLATE = '{color}{green}{summary}{color} from {bold}{start_time}{bold} to {bold}{end_time}{bold} @ {color}{blue}{location}{color}'

# Timer

@tornado.gen.coroutine
def timer(bot):
    # Execute events script
    bot.logger.info('Executing %s', __file__)
    command = ['python3', __file__, '--config-dir={}'.format(bot.config_dir)]
    environ = dict(os.environ, **{'PYTHONPATH': os.path.join(__file__, '..', '..') + ':' + os.environ.get('PYTHONPATH', '')})
    process = tornado.process.Subprocess(command, stdout=tornado.process.Subprocess.STREAM, env=environ)
    results = yield tornado.gen.Task(process.stdout.read_until_close)

    # Read configuration
    config_path      = os.path.join(bot.config_dir, 'events.yaml')
    events_config    = yaml.safe_load(open(config_path))
    templates        = events_config.get('templates', {})
    default_template = templates.get('default', TEMPLATE)

    # Read and process results
    for entry in json.loads(results):
        summary    = entry['summary']
        channels   = entry['channels']
        start_time = entry['start_time']
        end_time   = entry['end_time']
        location   = entry['location']

        # Send each entry to the appropriate channel
        for channel in channels:
            template = templates.get(channel, default_template)
            message  = bot.format_text(template,
                summary    = summary,
                start_time = start_time,
                end_time   = end_time,
                location   = location,

            )
            bot.send_message(message, channel=channel)

        # Mark entry as delivered
        bot.logger.info('Delivered %s to %s', summary, ', '.join(channels))

# Register

def register(bot):
    config_path   = os.path.join(bot.config_dir, 'events.yaml')
    events_config = yaml.safe_load(open(config_path))
    timeout       = events_config.get('timeout', 10*60)

    return (
        (timeout, timer),
    )

# Utility

def parse_recurrences(rrule, startdt, exclusions):
    rules      = dateutil.rrule.rruleset()
    first_rule = dateutil.rrule.rrulestr(rrule, dtstart=startdt)
    rules.rrule(first_rule)

    if not isinstance(exclusions, list):
        exclusions = [exclusions]

    for exdate in exclusions:
        try:
            for xdt in exdate.dts:
                rules.exdate(xdt.dt)
        except AttributeError:
            pass

    now   = datetime.datetime.now(datetime.timezone.utc)
    later = now + datetime.timedelta(days=1)
    for rule in rules.between(now, later):
        yield rule

# Script

def script(config_dir):
    # Open configuration
    config_path    = os.path.join(config_dir, 'events.yaml')
    events_config  = yaml.safe_load(open(config_path))
    events_timeout = events_config.get('timeout', 10*60)

    # Read events feeds
    entries          = []
    current_time     = time.time()
    logger           = logging.getLogger()

    for feed_config in events_config['feeds']:
        feed_url      = feed_config['url']
        feed_title    = feed_config['title']
        feed_channels = feed_config.get('channels', [])

        logger.info('Fetching %s (%s)', feed_title, feed_url)

        client  = tornado.httpclient.HTTPClient()
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Chrome/73.0.3683.105'}
        request = tornado.httpclient.HTTPRequest(feed_url, headers=headers, request_timeout=10
)
        try:
            result = client.fetch(request)
        except Exception as e:
            logger.warning(e)
            continue

        logger.info('Parsing %s (%s)', feed_title, feed_url)

        events = icalendar.Calendar.from_ical(result.body).walk('vevent')
        events = filter(lambda e: isinstance(e['DTSTART'].dt, datetime.datetime), events)

        for event in events:
            summary     = event.get('summary')
            startdt     = event.get('dtstart').dt
            enddt       = event.get('dtend').dt
            exclusions  = event.get('exdate')
            recurrences = event.get('rrule')
            description = event.get('description', '')
            location    = event.get('location', '')
            now         = datetime.datetime.now(datetime.timezone.utc)
            later       = now + datetime.timedelta(seconds=events_timeout)

            try:
                channels = re.findall(r'channels: (.*)', description)[0].split(',')
                channels = list(map(str.strip, channels))
            except (IndexError, TypeError, AttributeError):
                channels = feed_channels

            if recurrences:
                recurrences = recurrences.to_ical().decode('utf-8')
                starts      = parse_recurrences(recurrences, startdt, exclusions)
            else:
                starts      = [startdt]

            for start in starts:
                if now <= start <= later:
                    entries.append({
                        'summary'   : summary,
                        'start_time': start.strftime("%I:%M %p"),
                        'end_time'  : enddt.strftime("%I:%M %p"),
                        'location'  : location,
                        'channels'  : channels,
                    })

    # Dump entries as JSON
    json.dump(entries, sys.stdout)


# Main Execution

if __name__ == '__main__':
    tornado.options.define('config_dir', default=None,  help='Configuration directory')
    tornado.options.parse_command_line()
    options = tornado.options.options.as_dict()

    script(os.path.expanduser(options.get('config_dir', '~/.config/bobbit')))

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

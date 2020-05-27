# events.py

import datetime
import logging
import re

import icalendar
import dateutil

from bobbit.message import Message

# Metadata

NAME     = 'events'
ENABLE   = True
TEMPLATE = '{color}{green}{summary}{color} from {bold}{start_time}{bold} to {bold}{end_time}{bold} @ {color}{blue}{location}{color}'

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

# Timer

async def events_timer(bot):
    logger = logging.getLogger()

    # Read configuration
    config           = bot.config.load_module_config('events')
    timeout          = config.get('timeout', 10*60)
    templates        = config.get('templates', {})
    default_template = templates.get('default', TEMPLATE)

    # Read events feeds
    for feed_config in config.get('feeds', []):
        feed_url      = feed_config['url']
        feed_title    = feed_config['title']
        feed_channels = feed_config.get('channels', [])

        logger.info('Fetching %s (%s)', feed_title, feed_url)

        async with bot.http_client.get(feed_url) as response:
            text = await response.text()

        events = icalendar.Calendar.from_ical(text).walk('vevent')
        events = filter(lambda e: isinstance(e['DTSTART'].dt, datetime.datetime), events)
        logger.info('Parsing %s (%s)', feed_title, feed_url)

        # Check each event
        for event in events:
            summary     = event.get('summary')
            startdt     = event.get('dtstart').dt
            enddt       = event.get('dtend').dt
            exclusions  = event.get('exdate')
            recurrences = event.get('rrule')
            description = event.get('description', '')
            location    = event.get('location', '')
            now         = datetime.datetime.now(datetime.timezone.utc)
            later       = now + datetime.timedelta(seconds=timeout)

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
                if not now <= start <= later:
                    continue

                # Send each entry to the appropriate channel
                for channel in channels:
                    template = templates.get(channel, default_template)
                    await bot.outgoing.put(Message(
                        channel = channel,
                        body    = bot.client.format_text(
                            template,
                            summary    = summary,
                            start_time = start.strftime("%I:%M %p"),
                            end_time   = enddt.strftime("%I:%M %p"),
                            location   = location,
                        )
                    ))

                logger.info('Delivered %s to %s', summary, ', '.join(channels))

# Register

def register(bot):
    config  = bot.config.load_module_config('events')
    timeout = config.get('timeout', 10*60)

    if not config:
        return []

    return (
        ('timer', timeout, events_timer),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

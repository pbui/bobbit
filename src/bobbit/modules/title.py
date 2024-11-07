# title.py

import logging
import html
import json
import re

from bobbit.utils import strip_html

# Metadata

NAME    = 'title'
ENABLE  = True
PATTERN = r'.*(?P<url>https?://[^\s]+).*'
USAGE   = '''Usage: <url>
Looks up title of URL.
Example:
    > http://www.insidehighered.com/quicktakes/2019/06/24/uc-santa-cruz-removes-catholic-mission-bell
    Title: UC Santa Cruz Removes Catholic Mission Bell
'''

# Constants

CHANNEL_BLACKLIST = []
DOMAIN_BLACKLIST  = ['reddit.com', 'twitter.com']
AVOID_EXTENSIONS  = (
    '.gif', '.jpg', '.mkv', '.mov', '.mp4', '.png', '.jpeg', '.heic',
    '.gz' , '.xz' , '.bz2', '.tgz', '.deb',
)

# Generic Command

async def title(bot, message, url=None, override=False):
    url = url.rstrip('\x01')
    if not override and (message.channel in CHANNEL_BLACKLIST or \
        any(url.lower().endswith(extension) for extension in AVOID_EXTENSIONS) or \
        any(domain in url for domain in DOMAIN_BLACKLIST)):
        return

    async with bot.http_client.get(url) as response:
        # Skip non HTML content or content larger than 8MB
        if response.content_type != 'text/html' or \
           int(response.headers.get('Content-Length', 0)) > (1<<23):
            return

        try:
            text = (await response.text()).replace('\r', '').replace('\n', ' ')
            if not (
                (response := await mastodon_title(bot, url, text)) or
                (response := await photon_title(bot, url, text, message)) or
                (response := await youtube_title(bot, url, text))
            ):
                # XXX: If there are multiple titles, take the longest one (ugly workaround)
                html_title = sorted(re.findall(r'<title[^>]*>([^<]+)</title>', text), key=len)[-1]
                response   = bot.client.format_text(
                    '{color}{green}Title{color}: {bold}{title}{bold}',
                    title = strip_html(html.unescape(html_title)).strip()
                )
        except (IndexError, ValueError) as e:
            logging.warn(e)
            return

        return message.with_body(response)

async def photon_title(bot, url, text, message):
    if not re.search(r'<meta\s+name="keywords"\s+content="lemmy, client"', text):
        return None

    try:
        host, post = re.findall('post/([^/]+)/([0-9]+)', url)[0]
        return (await title(bot, message, f'https://{host}/post/{post}')).body
    except IndexError:
        return None

async def mastodon_title(bot, url, text):
    try:
        user   = re.findall(r'<meta content="([^"]+)" property="profile:username"', text)[0]
        status = re.findall(r'<meta content="([^"]+)" property="og:description"', text)[0]
        return bot.client.format_text(
            '{color}{green}{user}{color}: {bold}{status}{bold}',
            user    = user,
            status  = html.unescape(status).strip(),
        )
    except IndexError:
        return None

async def youtube_title(bot, url, text):
    # check that this is a YouTube *video* URL specifically
    if not any([
        re.search(r'https?://[^\s]+youtube.com/watch\?v=', url),
        re.search(r'https?://[^\s]+youtube.com/live/', url),
        re.search(r'https?://[^\s]+youtube.com/shorts/', url),
        re.search(r'https?://youtu.be/', url),
    ]):
        return None

    try:
        m = re.search(r'<script[^>]*>var\s+ytInitialData\s*=\s*(?P<data>\{.+\});</script>', text)
        if not m:
            raise re.error('No regex match')
        data = json.loads(m.group('data'))
        if '/shorts/' in url:
            details = data['overlay']['reelPlayerOverlayRenderer']['reelPlayerHeaderSupportedRenderers']['reelPlayerHeaderRenderer']
            video_name = details['reelTitleText']['runs'][0]['text']
            channel_name = details['channelTitleText']['runs'][0]['text']
        else:
            details = data['playerOverlays']['playerOverlayRenderer']['videoDetails']['playerOverlayVideoDetailsRenderer']
            video_name = details['title']['simpleText']
            channel_name = details['subtitle']['runs'][0]['text']

        return bot.client.format_text(
            '{color}{green}Video{color}: {bold}{video_name}{bold} {color}{green}Channel{color}: {bold}{channel_name}{bold}',
            video_name   = video_name.strip(),
            channel_name = channel_name.strip()
        )
    except (re.error, json.JSONDecodeError, IndexError, KeyError) as e:
        logging.warning('Unable to find channel or video name for %s, YouTube formatting may have changed: %s', url, e)
        return None

# Reddit Command

REDDIT_PATTERN = r'.*(?P<url>https?://[^\s]*reddit.com/[^\s]+).*'
REDLIB_HOST    = 'redlib.h4x0r.space'

async def reddit_title(bot, message, url):
    # XXX: Hack is to redirect to redlib instance
    url = re.sub(r'://([^/]+)/', '://{}/'.format(REDLIB_HOST), url)

    async with bot.http_client.get(url) as response:
        text = await response.text()

        try:
            post_title = re.findall(r'<meta property="og:title" content="([^"]+)"', text)[0]
            post_title, subreddit = post_title.split(' - ', 1)
            return message.with_body(bot.client.format_text(
                '{color}{green}{}{color}: {bold}{}{bold}',
                subreddit, html.unescape(post_title)
            ))
        except IndexError:
            pass

        try:
            post_title = re.findall(r'shreddit-title title="([^"]+)"', text)[0]
            post_title, subreddit = post_title.rsplit(' : ', 1)
            return message.with_body(bot.client.format_text(
                '{color}{green}{}{color}: {bold}{}{bold}',
                subreddit, html.unescape(post_title)
            ))
        except IndexError:
            pass

        return await title(bot, message, url, True)

# Register

def register(bot):
    global CHANNEL_BLACKLIST

    config = bot.config.load_module_config('title')
    CHANNEL_BLACKLIST = config.get('blacklist', CHANNEL_BLACKLIST)

    if config.get('disabled', False):
        return []

    return (
        ('command', PATTERN       , title),
        ('command', REDDIT_PATTERN, reddit_title),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

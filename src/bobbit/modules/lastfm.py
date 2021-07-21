# lastfm.py

# Metadata

NAME = "lastfm"

PATTERN = r'^!np (?P<lastfm_account>.*$)'
ENABLE = True
USAGE = '''!np <lastfm_account>
Gets the lastfm scrobble information for the given account
Example:
  > !np AndroidKitKat
  Now playing: Android KitKat - I Can't Sleep
  -- OR --
  > !np AndroidKitKat
  AndroidKitKat is not listening to anything right now.
'''

# Constants

# Load these from file to prevent hardcoding!
API_KEY = None
API_URL = "http://ws.audioscrobbler.com/2.0/?"

# ?method=user.getrecenttracks"
#&user={}&api_key={}&format=json"

# Helper functions

async def get_play_count(bot, lastfm_account, track, artist):
  URL_PARAMS = {
    "method": "track.getInfo",
    "user": lastfm_account,
    "track": track,
    "artist": artist,
    "api_key": API_KEY,
    "format": "json"
  }
  async with bot.http_client.get(API_URL, params=URL_PARAMS) as resp:
    data = await resp.json()
    # I don't need to handle errors here, because the API will return an error if the track isn't found!
    return data.get("track", {}).get("userplaycount", 0)

# Command
async def lastfm(bot, message, lastfm_account=None):
  if lastfm_account is None:
    return message.with_body("Please provide a LastFM account")
  URL_PARAMS = {
    "method": "user.getrecenttracks",
    "user": lastfm_account,
    "api_key": API_KEY,
    "format": "json"
  }
  async with bot.http_client.get(API_URL, params=URL_PARAMS) as resp:
    data = await resp.json()
    if data.get("error"):
      return message.with_body(data.get("message"))
    
    tracks = data.get("recenttracks", {}).get("track", [])
    if not tracks:
      return message.with_body(f"{lastfm_account} has never listened to anything")

    # look at track 0, and get the artist and track name!   
    track = tracks[0]
    artist = track.get("artist", {}).get("#text", "")
    album = track.get("album", {}).get("#text", "")
    name = track.get("name", "")

    # get the play count
    play_count = await get_play_count(bot, lastfm_account, name, artist)

    # look for nowplaying
    nowplaying = track.get("@attr", {}).get("nowplaying", {})
    if not nowplaying:
      date = track.get("date", {}).get("uts", "")
      return message.with_body(f"{lastfm_account} last listened to {name} by {artist} from the album {album} [Playcount: {play_count}]")
    else:
      return message.with_body(f"{lastfm_account} is listening to {name} by {artist} from the album {album} [Playcount: {play_count}]")


# Register

def register(bot):
  global API_KEY
  config = bot.config.load_module_config("lastfm")
  API_KEY = config.get('api_key', '')

  if API_KEY is None:
    return []
  
  return (
    ('command', PATTERN, lastfm),
  )

# vim: set sw=4 ts=8 expandtab ft=python:

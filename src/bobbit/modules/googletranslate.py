# googletranslate.py

from bobbit.utils import parse_options

# Metadata

NAME    = 'googletranslate'
ENABLE  = True
PATTERN = '^!gt (?P<query>.*$)'
USAGE   = '''Usage: !gt <query>
Translate an input string from a source language to a target language using
google translate

    -s <language>   source language (default: automatically detect)
    -t <language>   target language (default: English)

Examples:
    > !gt por favor
    please
    > !gt -s German -t French Rad
    la roue
'''

# Constants

GT_URL      = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl='
LANGUAGE_CODES = {
    "am": "amharic",
    "ar": "arabic",
    "eu": "basque",
    "bn": "bengali",
    "en-GB": "english (uk)",
    "pt-BR": "portuguese (brazil)",
    "bg": "bulgarian",
    "ca": "catalan",
    "chr": "cherokee",
    "hr": "croatian",
    "cs": "czech",
    "da": "danish",
    "nl": "dutch",
    "en": "english (us)",
    "et": "estonian",
    "fil": "filipino",
    "fi": "finnish",
    "fr": "french",
    "de": "german",
    "el": "greek",
    "gu": "gujarati",
    "iw": "hebrew",
    "hi": "hindi",
    "hu": "hungarian",
    "is": "icelandic",
    "id": "indonesian",
    "it": "italian",
    "ja": "japanese",
    "kn": "kannada",
    "ko": "korean",
    "lv": "latvian",
    "lt": "lithuanian",
    "ms": "malay",
    "ml": "malayalam",
    "mr": "marathi",
    "no": "norwegian",
    "pl": "polish",
    "pt-PT": "portuguese (portugal)",
    "ro": "romanian",
    "ru": "russian",
    "sr": "serbian",
    "zh-CN": "chinese (prc)",
    "sk": "slovak",
    "sl": "slovenian",
    "es": "spanish",
    "sw": "swahili",
    "sv": "swedish",
    "ta": "tamil",
    "te": "telugu",
    "th": "thai"
}

# Command

def match_code(lang, default):
    if lang in LANGUAGE_CODES:
        return lang

    lang = lang.lower()
    for code, name in LANGUAGE_CODES.items():
        if lang in name:
            return code

    return default

async def googletranslate(bot, message, query, source='auto', target='en'):
    options, query = parse_options({'-s': source, '-t': target}, query)
    source = match_code(options['-s'], 'auto')
    target = match_code(options['-t'], 'en')

    complete_url = GT_URL + f'{source}&tl={target}&dt=t&q={query}'

    async with bot.http_client.get(complete_url) as response:
        try:
            response = (await response.json())[0][0][0]
        except (IndexError, ValueError):
            response = 'No results'

    return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, googletranslate),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

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
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'zh': 'chinese',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jv': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'rw': 'kinyarwanda',
    'ko': 'korean',
    'ku': 'kurdish',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar',
    'my': 'burmese',
    'ne': 'nepali',
    'no': 'norwegian',
    'ny': 'nyanja',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'si': 'sinhalese',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tl': 'tagalog',
    'tl': 'filipino',
    'tg': 'tajik',
    'ta': 'tamil',
    'tt': 'tatar',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'tk': 'turkmen',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'
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

    if query in bot.users:
        try:
            history = bot.history.search(message.channel, nick=query, limit=1, reverse=True)
            query = list(history)[0].body
        except IndexError:
            pass

    query = query.rstrip()
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

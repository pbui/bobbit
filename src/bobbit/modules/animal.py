# animal.py

import logging
from bobbit.message import Message
import random
import requests
import re

NAME = 'animal'
ENABLE = True
PATTERN = r'^![Aa]nimal+(?P<phrase>.*)$'
USAGE = '''Usage: !animal [options] 
Print a random ascii animal
    -a [animal] print a specific animal
Example:
    > !animal -a monkey
'''

#list
CATEGORY =  ['aardvarks','amoeba','bats','bears','beavers','birds-land','birds-water','bisons','camels','cats','cows','deer','dogs','dolphins','elephants','fish','frogs','horeses','marsupials','monkeys','moose','other-land','other-water','rabbits','rhinoceros','scorpions','spiders','wolves','insects','repties','rodents']
INSECTS = ['ants','bees','beetles','butterflies','caterpillars','cockroaches','other','snails','worms']
REPTILES = ['alligators','dinosaurs','lizards','snakes','turtles']
RODENTS = ['mice','other']

#commmand

def getArt(selection = None):
    URL = 'https://www.asciiart.eu/animals'
    if(not selection):
        cat = CATEGORY[random.randint(0,len(CATEGORY)-1)]
    elif(any(a.startswith(selection) for a in CATEGORY)):
        cat = next(filter(lambda a : a.startswith(selection), CATEGORY))
    elif(any(a.startswith(selection) for a in INSECTS)):
        cat = 'insects'
    elif(any(a.startswith(selection) for a in REPTILES)):
        cat = 'reptiles'
    elif(any(a.startswith(selection) for a in RODENTS)):
        cat = 'rodents'

    URL = URL + '/' + cat 

    if(not selection):
        if(cat == 'insects'):
            URL = URL + '/' + INSECTS[random.randint(0,len(INSECTS)-1)]
        if(cat == 'reptiles'):
            URL = URL + '/' + REPTILES[random.randint(0,len(REPTILES)-1)]
        if(cat == 'rodents'):
            URL = URL + '/' + RODENTS[random.randint(0,len(RODENTS)-1)]
    elif(any(a.startswith(selection) for a in INSECTS)):
        URL = URL + '/' +   next(filter(lambda a : a.startswith(selection), INSECTS)) 
    elif(any(a.startswith(selection) for a in REPTILES)):
        URL = URL + '/' +   next(filter(lambda a : a.startswith(selection), REPTILES))
    elif(any(a.startswith(selection) for a in RODENTS)):
        URL = URL + '/' +   next(filter(lambda a : a.startswith(selection), RODENTS))
        
    
    response = requests.get(URL)
    data = response.text
    art = re.findall(r'(.*)</pre>',data,flags=re.DOTALL)
    if(len(art)>0):
        art = art[0].split('</pre>')
        if(len(art) > 0):
            pic = art[random.randint(0,len(art)-1)]
            while(pic.find('<pre class="p-0 m-0 text-dark">') >=0 or pic.find('<pre class="mt-1 mb-0 text-dark d-none d-sm-block">')>=0):
                return getArt(selection)
            while(pic.find('">')>=0):
                pic = pic[pic.find('">')+2:]
                if(pic==None):
                    return getArt(selection)
            return pic
        else:
            return getArt(selection)
    else:
       return getArt(selection)



async def animal(bot,message,phrase=None):
    #get animal selection if there is one
    selection = None
    badSelect = False

    if(phrase and phrase.find('-a') >= 0):
        selection = phrase[phrase.find('-a'):]
        selection = selection.split()[-1].strip()

    if(selection and (not any(a.startswith(selection) for a in CATEGORY) and not any(a.startswith(selection) for a in INSECTS) and not any(a.startswith(selection) for a in REPTILES) and not any(a.startswith(selection) for a in RODENTS))):
        return 'Bad animal'
        return message.with_body('Bad animal')

    pic = getArt(selection)
    pic = pic.replace(r'\\n', r'\\\\n')

    return message.with_body(pic)



def register(bot):
    return (
        ('command', PATTERN, animal),
    )

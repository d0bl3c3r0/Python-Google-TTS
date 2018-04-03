#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import hashlib
import os
import sys
import argparse
import shutil

# Define a few maps for reference
namemap = {
            "nl-NL" : [
                "nl-NL-Standard-A"
                ],
            "en-AU" : [
                "en-AU-Standard-A",
                "en-AU-Standard-B",
                "en-AU-Standard-C",
                "en-AU-Standard-D"
                ],
            "en-GB" : [
                "en-GB-Standard-A",
                "en-GB-Standard-B",
                "en-GB-Standard-C",
                "en-GB-Standard-D"
                ],
            "en-US" : [
                "en-US-Standard-A",
                "en-US-Standard-B",
                "en-US-Standard-C",
                "en-US-Standard-D",
                "en-US-Standard-E",
                "en-US-Wavenet-A",
                "en-US-Wavenet-B",
                "en-US-Wavenet-C",
                "en-US-Wavenet-D",
                "en-US-Wavenet-E",
                "en-US-Wavenet-F",
                ],
            "fr-FR" : [
                "fr-FR-Standard-C",
                "fr-FR-Standard-D",
                ],
            "fr-CA" : [
                "fr-CA-Standard-A",
                "fr-CA-Standard-B",
                "fr-CA-Standard-C",
                "fr-CA-Standard-D"
                ],
            "de-DE" : [
                "de-DE-Standard-A",
                "de-DE-Standard-B"
                ],
            "ja-JP" : [
                "ja-JP-Standard-A"
                ],
            "pt-BR" : [
                "pt-BR-Standard-A"
                ],
            "es-ES" : [
                "es-ES-Standard-A"
                ],
            "sv-SE" : [
                "sv-SE-Standard-A"
                ],
            "tr-TR" : [
                "tr-TR-Standard-A"
                ]
            }
    
formatmap = {
    "LINEAR16" : "wav",
    "MP3" : "mp3",
    "OGG_OPUS" : "ogg"
}

sampleratemap = [
    8000,
    16000,
    22050,
    44100,
    48000
]

# Get config from CLI args
i = 0
argsDict = {}
for item in sys.argv:
    if i == 0:
        i = i + 1
        pass
    else:
        i = i + 1
        paramname, paramval = item.partition(
            "="
            )[::2]
        argsDict[paramname] = paramval

try:
    helpReq = argsDict['--help']
    print ("")
    print (
        "Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"en-US-Standard-B\" --fileformat=LINEAR16 --samplerate=16000 --apikey=YOUR-API-KEY --text=\"Hello World\"".format(
            sys.argv[0]
            )
        )
    print ("")
    print ("--cache         : Location of file cache. Useful if you repeatedly request")
    print ("                      the same text to speech and wish to conserve bandwidth")
    print ("                      and reduce Azure costs. Must be writeable.")
    print ("--dest          : Location for the output file. Must be writeable.")
    print ("--lang          : Language to be spoken. Case sensitive.")
    print ("--voice         : Voice to be used. Case sensitive.")
    print ("--fileformat    : Format of the output file. (optional)")
    print ("--samplerate    : Sample rate for generated file (optional).")
    print ("--apikey        : API key generated by Google Cloud.")
    print ("--text          : Text to convert to speech. MUST be enclosed in double quotes.")
    print ("")
    print ("Available language combinations (--lang --voice):")
    for item, value in namemap.items():
        for voiceval in value:
            print (
                "Language: {}   Voice: {}".format(
                    item,
                    voiceval
                    )
                )
    print ("")
    print ("Available file formats:")
    for item, value in formatmap.items():
        print (item)
    sys.exit(1)
except:
    pass
    
    

try:
    destLoc = argsDict['--dest']
except:
    print ("")
    print ("Error: destination location not specified.")
    print ("")
    print (
        "Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"en-US-Standard-B\" --fileformat=LINEAR16 --samplerate=16000 --apikey=YOUR-API-KEY --text=\"Hello World\"".format(
            sys.argv[0]
            )
        )
    print ("")
    sys.exit(1)

try:
    ttsLang = argsDict['--lang']
except:
    print ("")
    print ("Error: language not specified.")
    print ("")
    print (
        "Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"en-US-Standard-B\" --fileformat=LINEAR16 --samplerate=16000 --apikey=YOUR-API-KEY --text=\"Hello World\"".format(
            sys.argv[0]
            )
        )
    print ("")
    sys.exit(1)
    
try:
    ttsVoice = argsDict['--voice']
except:
    print ("")
    print ("Error: voice not specified.")
    print ("")
    print (
        "Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"en-US-Standard-B\" --fileformat=LINEAR16 --samplerate=16000 --apikey=YOUR-API-KEY --text=\"Hello World\"".format(
            sys.argv[0]
            )
        )
    print ("")
    sys.exit(1)

try:
    ttsFormat = argsDict['--fileformat']
except:
    print ("Warning: file format not specified. Assuming LINEAR16")
    ttsFormat = "LINEAR16"


try:
    ttsSamplerate = int(argsDict['--samplerate'])
except:
    print ("Warning: Samplerate not specified or invalid. Assuming 16000")
    ttsSamplerate = 16000
    
try:
    ttsText = argsDict['--text']
except:
    print ("")
    print ("Error: text not specified.")
    print ("")
    print (
        "Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"en-US-Standard-B\" --fileformat=LINEAR16 --samplerate=16000 --apikey=YOUR-API-KEY --text=\"Hello World\"".format(
            sys.argv[0]
            )
        )
    print ("")
    sys.exit(1)

try:
    ttsApiKey = argsDict['--apikey']
except:
    print ("")
    print ("Error: API key not specified.")
    print ("")
    print (
        "Usage: {} --cache=/path/to/cache --dest=/path/to/destination --lang=en-US --voice=\"en-US-Standard-B\" --fileformat=LINEAR16 --samplerate=16000 --apikey=YOUR-API-KEY --text=\"Hello World\"".format(
            sys.argv[0]
            )
        )
    print ("")
    sys.exit(1)    

try:
    ttsCache = argsDict['--cache']
except:
    ttsCache = None

if ttsVoice not in namemap[ttsLang]:
    print ("")
    print ("Error: invalid language or Voice specified, or invalid combination: The following language/Voice combinations are available:")
    print ("")
    for item, value in namemap.items():
        for voiceval in value:
            print (
                "Language: {}".format(
                    item
                    )
                )
            print (
                "Language: {}   Voice: {}".format(
                    item, voiceval
                    )
                )
    sys.exit(1)
    
if ttsFormat not in formatmap:
    print ("")
    print ("Error: invalid format specified: The following formats are available:")
    print ("")
    for item, value in formatmap.items():
        print (item)
    sys.exit(1)

if ttsSamplerate not in sampleratemap:
    print ("")
    print ("Error: invalid sample rate specified: The following formats are available:")
    print ("")
    for item in sampleratemap:
        print (item)
    sys.exit(1)
    
if ttsCache:
    cacheaccess = os.access(ttsCache, os.W_OK)
    if not cacheaccess:
        print ("Cannot write to cache location, ignoring --cache setting...")
        ttsCache = None

m = hashlib.md5()
# Hash lang+Voice+text
m.update(
    (
        "{}-{}-{}-{}-{}".format(
            ttsLang,
            ttsVoice,
            ttsText,
            ttsFormat,
            ttsSamplerate
            )
        ).encode(
            'utf-8'
            )
        )
# create filename base on MD5 hash

filename = "{}.{}".format(
    m.hexdigest(),
    formatmap[ttsFormat]
    )
if ttsCache:
    # If our file already exists, just return it so we don't have to do an API call...
    if os.path.isfile(os.path.join(ttsCache, filename)):
        try:
            shutil.copy2(
                os.path.join(
                    ttsCache,
                    filename
                    ),
                destLoc
                )
            sys.exit(0)
        except (Exception) as e:
            print (
                "Could not copy cached file: {}".format(
                    e
                    )
                )
            print ("Exiting...")
            sys.exit(1)

# Wait to import this until after we check cache to keep things as speedy as possible...
from googletts import Translator
translator = Translator(ttsApiKey)
try:
    data = translator.speak(
        ttsText.encode(
            'utf-8'
            ).decode(
                'latin-1'
                ),
            ttsLang,
            ttsVoice,
            ttsFormat,
            ttsSamplerate
            )
except (Exception) as e:
    print (
        "Error retrieving speech file: {}".format(
            e
            )
        )
    sys.exit(1)

if ttsCache:
    try:
        with open(destLoc, 'wb') as f:
            f.write(data)
    except (Exception) as e:
        print (
            "Couldn't write to file {}: {}".format(
                destLoc,
                e
                )
            )
        sys.exit(1)
    try:
        with open(os.path.join(ttsCache, filename), 'w') as f:
            f.write(data)
    except (Exception) as e:
        cacheFileLoc = os.path.join(
            ttsCache,
            filename
            )
        print (
            "Couldn't write to file {}: {}".format(
                cacheFileLoc,
                e
                )
            )
        sys.exit(1)
else:
    try:
        with open(destLoc, 'wb') as f:
            f.write(data)
    except (Exception) as e:
        print (
            "Couldn't write to file {}: {}".format(
                destLoc,
                e
                )
            )
        sys.exit(1)
        
sys.exit(0)
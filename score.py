""" Requires sox and text2wave (via festival)
"""

from pippi import dsp
from pippi import tune
import subprocess
import os

def sox(cmd, sound):
    path = os.getcwd()
    filename_in = '/proc-in'
    filename_out = '/proc-out.wav'

    dsp.write(sound, filename_in)

    cmd = cmd % (path + filename_in + '.wav', path + filename_out)
    subprocess.call(cmd, shell=True)

    sound = dsp.read(path + filename_out).data

    return sound

def text2wave(lyrics):
    path = os.getcwd() + '/bag.wav'
    cmd = "echo '%s' | /usr/bin/text2wave -o %s" % (lyrics, path)

    ret = subprocess.call(cmd, shell=True)

    words = dsp.read('bag.wav').data

    return words

def singit(lyrics, mult):
    words = text2wave(lyrics)

    pitches = [ dsp.randint(1, 10) for i in range(dsp.randint(2, 4)) ]
    pitches = tune.fromdegrees(pitches, octave=dsp.randint(1, 4), root='a')

    sings = [ dsp.pine(words, dsp.flen(words) * mult, pitch) for pitch in pitches ]
    sings = dsp.mix(sings)

    sings = sox("sox %s %s tempo 5.0", sings)

    return sings

verses = [
        'sing a ling a ling a', 
        'ding ling a sing ling ding a', 

        'ee oh ee oh see low', 
        'me low see low tree low',

        'ping a ding a ding a', 
        'sling ding a bing ling ding a', 

        'ee oh ee oh see low', 
        'me low see low tree low',

        'sing a ling a ling a', 
        'ding ling a sing ling ding a', 

        'ee oh ee oh see low', 
        'me low see low tree low',


        ]

layers = []

# v1: 1 layers, 50 - 1000 mult
# v2: 3 layers, 50 - 1000 mult
# v3: 2 layers, 50 - 100 mult

for l in range(2):
    out = ''.join([ singit(lyric, dsp.randint(50, 100)) for lyric in verses ])

    layers += [ out ]

out = dsp.mix(layers)

dsp.write(out, 'sing')

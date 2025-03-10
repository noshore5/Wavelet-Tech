import numpy as np
from keys import *
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import sounddevice as sd
import math
import Envelope as en
from Envelope import *
from TuneRequests import *


filename = 'reels.txt'

def compute_accidentals(key):
    offsets = [0,2,4,5,7,9,11]
    for n,i in enumerate(modes):
        if i == key[1]:
            offset = offsets[n]
    semitones = universal_encoder[key[0]] - offset
    while semitones%7 != 0:
        semitones = semitones+12
    accidentals = semitones/7
    return int(accidentals)

def abc_to_notestring(abc_string):
        notes = [char for char in abc_string if char.isalpha() or char.isnumeric() or char == '(' or char.startswith(('^','='))]
        i,output = 0,[]
        while i < len(notes):
            if notes[i] == '(' and i+2 < len(notes):
                output.append(notes[i+2])
                output.append(notes[i+4])
                i+=5
            else:
                output.append(notes[i])
                i+=1
        notes = output
        # good as long as measures can have no more than 4 beats
        for n,i in enumerate(notes):
            if i == '2':
                notes[n] = notes[n-1]
            if i == '3':
                notes[n] = notes[n-1]
                notes.insert(n,notes[n-1])
            if i == '4':
                notes[n] = notes[n-1]
                notes.insert(n,notes[n-1])
                notes.insert(n,notes[n-1]) 
        return notes

    #Write later to deal with accidentals, rolls and cuts
def abc_to_fancy_notestring(abc_string):
    notes = [char for char in abc_string if char.isalpha() or char in ['#', '~','('] or char.isnumeric()]

def constructor(tune,instrument,duration= .2):
    instrument = instrument.lower()
    inst = True
    construction = []
    for i in tune.tones:
        frequency = 261.6*2**(i/12) # low c root
        if instrument == 'piano':
            waveform = piano_note(frequency,duration,8000)
        elif instrument == 'banjo':
            waveform = banjo_note(frequency,duration,8000)
        elif instrument == 'sine':
            waveform = sine_note(frequency,duration,8000)
        elif instrument == 'naked sine':
            waveform = sine_note(frequency,duration,8000,envel=False)
        else:
            waveform = piano_note(frequency,duration,8000)
            inst = False
        construction.append(waveform)
    if inst == False:
        print('Invalid instrument, defaulting to piano')
    construction.append(waveform)
    return [x for xs in construction for x in xs]

def semitone_input(tones):
    inv_map = {v: k for k, v in universal_encoder.items()}
    abc = [inv_map[i] for i in tones]
    return abc

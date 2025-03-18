import numpy as np
import dbreader
from keys import *
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import sounddevice as sd
import math
import Envelope as en
from Envelope import *
from TuneRequests import *
from dbreader import *
from TuneClass import *

def originalentry(tune,mankey):
    if type(tune) == str:
        if not any(char in tune for char in 'hijklmnopqrstuvwxy'):
            abc_notation = tune.strip()
        else:
            raise Exception('Try again')

    elif type(tune[0]) == int: 
        abc_notation = semitone_input(tune)
    
    elif type(tune[0]) == str:
        notes = tune
        if mankey != 0:
            key = choose_key(mankey)
        else:
            raise Exception('Please Enter Manual Key')
        return 
    
    if mankey != 0:
        key = choose_key(mankey)
    else:
        raise Exception('Please Enter Manual Key')
    return key, abc_notation, notes,

class Tune:
    def __init__(self,tune,mankey = 0):
        setting = 1
        self.Posssible_Instruments = ['Piano','Banjo','Sine']
        #preprocess here
        df, num_settings = initializer(tune,setting)
        self.num_settings = num_settings
        for index, value in df.items():
            setattr(self, index, value)
        self.key = choose_key(self.mode)
        #try:
            # make viable for original entry
        #except:
         #   self.key, self.abc, self.notes = originalentry(tune,mankey)
        # need to pull composer, key, dance, and abc from dataframe
        self.setting = f'Setting {setting} of {num_settings}'
        self.abc_cleaned = self.abc
        self.notes = abc_to_notestring(self.abc_cleaned)
        self.notes = keychanger(self,self.key)
        self.tones = notes_to_semitones2(self,universal_encoder)

    def play(self,duration = .125,instrument='piano'):
        waveform = constructor(self,instrument,duration)
        waveform = np.float32(waveform)
        self.waveform = waveform
        sd.play(waveform,samplerate=44100)
        sd.wait()

    def changekey(self,new_key):
        new_key = choose_key(new_key)
        self.notes = keychanger(self,new_key)
        self.key = new_key
        self.tones = notes_to_semitones2(self,universal_encoder)
    
    def changesetting(self, setting):
        sets,_ =initializer(self.name,setting) 
        for index, value in sets.items():
            setattr(self, index, value)
        self.key = choose_key(self.mode)
        self.setting = f'Setting {setting} of {self.num_settings}'
        print(self.setting)
        self.abc_cleaned = self.abc
        self.notes = abc_to_notestring(self.abc_cleaned)
        self.notes = keychanger(self,self.key)
        self.tones = notes_to_semitones2(self,universal_encoder)
        return self
        
def main(): 
    t = input('Enter Tune Name').lower()
    tune = Tune(t)
    tuneactions = dir(tune)[28:]
    action = True
    while action != 'quit':
        action = input(f'Possible requests: {tuneactions} or quit, or next').lower()
        try:
            attr = getattr(tune,action)
            print(attr)
        except:
            if action == 'play()':
                args1 = input('Duration of Quarter Note:\n')
                args2 = input('Instrument:\n').lower()
                kwargs = {}
                if args1:
                    kwargs['arg1'] = args1
                if args2:
                    kwargs['arg2'] = args2
                tune.play(**kwargs)
            elif action == 'changesetting()':
                args1 = input('Setting:\n')
                tune.changesetting(args1)
            elif action == 'changekey()':
                tune.changekey(input('Enter new key:\n'))
            elif action =='quit':
                break
            elif action == 'next':
                main()
                action = 'quit'
            else:
                print('Action not recognized')

    print('Goodbye')
        
        
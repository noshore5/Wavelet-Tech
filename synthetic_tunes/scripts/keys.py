import TuneClass as tc

universal_encoder={'G,':-5,'^G,':-4,'A,':-3,'^A,':-2,'B,':-1,
                   'C':0,'^C':1,'D':2,'^D':3,'E':4,
                   'F':5,'^F':6,'G': 7,'^G':8,'A':9,'^A':10,
                   'B': 11,'c':12,'^c': 13,
                   'd': 14,'^d':15,'e':16,'f':17,'^f':18,
                   'g':19,'^g':20,'a':21,'^a':22,'b':23,'c.':24,
                   '^c.':25,'d.':26,'^d.':27,'e.':28,'f.':29,
                   '^f.':30,'g.':31,'^g.':32,'a.':33,'b.':34}

modes = ['Ionian','Dorian','Phrygian',
         'Lydian','Mixolydian','Aeolian',
         'Locrian']


def choose_key(key):
    # input looks like 'Edor'
    if type(key) == tuple:
        m = key[1]
        k = key[0]
    elif type(key) == str:
        key = key.replace(' ','')
        k = key[0]
        m = key[1:4]
        if m.lower() == 'maj':
            m = modes[0]
        if m.lower() == 'min':
            m = modes[-2]
        for i in modes:
            if m.lower() == i.lower()[0:3]:
                m = i
    else:
        raise Exception('Invalid valid key')
    return (k.upper(),m)

def notes_to_semitones(tune,custom_mapping):
    key = tune.key
    note_string = tune.notes
    accidentals = tc.compute_accidentals(key)
    numbers = [custom_mapping[note] for note in note_string if note in custom_mapping]
    # need to rewrite to for all possible keys
    if accidentals == 1:
        for i,n in enumerate(numbers):
            if n  == 41%12:
                numbers[i]=6
            if n==17:
                numbers[i]=18
    if accidentals == 2:
        for i,n in enumerate(numbers):
            if n==0:
                numbers[i]=0
            if n == 5:
                numbers[i]=6
            if n==12:
                numbers[i]=13
            if n==17:
                numbers[i]=18
    if accidentals == 3:
        for i,n in enumerate(numbers):
            if n==0:
                numbers[i]=1
            if n == 5:
                numbers[i]=6
            if n==7:
                numbers[i] = 8
            if n==12:
                numbers[i]=13
            if n==17:
                numbers[i]=18
            if n == 19:
                numbers[i] = 20
    if accidentals == -1:
        for i,n in enumerate(numbers):
            if n == 11:
                numbers[i]=10
            if n==23:
                numbers[i]=22
    if accidentals == -2:
        for i,n in enumerate(numbers):
            if n==4:
                numbers[i]=3
            if n == 11:
                numbers[i]=10
            if n==16:
                numbers[i]=15
            if n==23:
                numbers[i]=22
    
    return numbers

def add_accidentals(numbers,accidentals):
    if accidentals > 0:
        for i,n in enumerate(numbers):
            if n%12 == (7*accidentals-2)%12:
                numbers[i]+=1
        accidentals -= 1
        add_accidentals(accidentals,numbers)



def ionian(semitones):
    """Convert to Ionian (C major). No changes needed."""
    return semitones

def dorian(semitones):
    for i, note in enumerate(semitones):
        # Lower the 3rd (E to D#)
        if note % 12 == 4 % 12:
            semitones[i] -= 1
        # Lower the 7th (B to A#)
        if note % 12 == 11 % 12:
            semitones[i] -= 1
    return semitones

def phrygian(semitones):
    """Convert from C Major (Ionian) to C Phrygian."""
    for i, note in enumerate(semitones):
        if note % 12 == 2 % 12:  # Lower the 2nd (D to C#)
            semitones[i] -= 1
        if note % 12 == 4 % 12:  # Lower the 3rd (E to D#)
            semitones[i] -= 1
        if note % 12 == 9 % 12:  # Lower the 6th (A to G#)
            semitones[i] -= 1
        if note % 12 == 11 % 12:  # Lower the 7th (B to A#)
            semitones[i] -= 1
    return semitones

def lydian(semitones):
    """Convert from C Major (Ionian) to C Lydian."""
    for i, note in enumerate(semitones):
        if note % 12 == 5 % 12:  # Raise the 4th (F to F#)
            semitones[i] += 1
    return semitones

def mixolydian(semitones):
    """Convert from C Major (Ionian) to C Mixolydian."""
    for i, note in enumerate(semitones):
        if note % 12 == 11 % 12:  # Lower the 7th (B to A#)
            semitones[i] -= 1
    return semitones

def aeolian(semitones):
    """Convert from C Major (Ionian) to C Aeolian (Natural Minor)."""
    for i, note in enumerate(semitones):
        if note % 12 == 4 % 12:  # Lower the 3rd (E to D#)
            semitones[i] -= 1
        if note % 12 == 9 % 12:  # Lower the 6th (A to G#)
            semitones[i] -= 1
        if note % 12 == 11 % 12:  # Lower the 7th (B to A#)
            semitones[i] -= 1
    return semitones

def locrian(semitones):
    """Convert from C Major (Ionian) to C Locrian."""
    for i, note in enumerate(semitones):
        if note % 12 == 2 % 12:  # Lower the 2nd (D to C#)
            semitones[i] -= 1
        if note % 12 == 4 % 12:  # Lower the 3rd (E to D#)
            semitones[i] -= 1
        if note % 12 == 7 % 12:  # Lower the 5th (G to F#)
            semitones[i] -= 1
        if note % 12 == 9 % 12:  # Lower the 6th (A to G#)
            semitones[i] -= 1
        if note % 12 == 11 % 12:  # Lower the 7th (B to A#)
            semitones[i] -= 1
    return semitones

def remove_accidentals(semitones):    
    for i,note in enumerate(semitones):
            if note%12 == 1%12:
                semitones[i] +=1
            if note%12 == -2%12:
                semitones[i] += 1
            if note%12 == -4%12:
                semitones[i] += 1
            if note%12 == 3 %12:
                semitones[i] += 1
            if note%12 == 6%12:
                semitones[i] -= 1
        
    # Map all notes to C major
    return semitones

def notes_to_semitones2(tune,custom_mapping):
    note_string = tune.notes
    numbers = [custom_mapping[note] for note in note_string if note in custom_mapping]
    return numbers

def keychanger(tune,new_key):
    # first make key c
    key = tune.key
    new_key = choose_key(new_key)
    semitones = notes_to_semitones2(tune,universal_encoder)
    offset = universal_encoder[key[0]]
    normed = [tone - offset for tone in semitones]
    # now its in c, need to get rid of accidentals
    remove_accidentals(normed)

    call = new_key[1]
    dispatcher = {'Ionian':ionian,'Dorian': dorian, 'Phrygian':phrygian,'Lydian':
                  lydian,'Mixolydian':mixolydian,'Aeolian':aeolian,'Locrian':locrian}
    dispatcher[call](normed)

    # go to new key by offset
    tones = [i+universal_encoder[new_key[0]] for i in normed]
    
    notes = [{value: key for key, value in universal_encoder.items()}[i] for i in tones]
    #tune.notes = notes
    
    return notes

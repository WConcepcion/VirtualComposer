import numpy as np
import itertools
import random as r
from midiutil import MIDIFile
import seaborn as sns
import matplotlib.pyplot as plt

## Generate Rules and Seed for automata

def generate3statesRandomRule(r_size) :
    x = [0,1,2]
    permutation = [p for p in itertools.product(x, repeat=2*r_size+1)]
    rule = {}
    for i in permutation :
        rule[i] = r.choices([0,1,2],weights = [0.5,0.25,0.25])[0]
    return(rule)

def generateRandomRule(r_size) :
    x = [0,1]
    permutation = [p for p in itertools.product(x, repeat=2*r_size+1)]
    rule = {}
    for i in permutation :
        rule[i] = r.choice([0,1])
    return(rule)


def generateSingleSeed(size) :
    seed = [ 0 for i in range(size)]
    seed[r.randint(0,size-1)] = 1
    return(seed)

def generateSeed(size,seed_density) :
    return([ r.choices([0,1], weights = [1- seed_density, seed_density])[0] for i in range(size)])

def random_sum_to(n, num_terms = None):
    num_terms = (num_terms or r.randint(2, n)) - 1
    a = r.sample(range(1, n), num_terms) + [0, n]
    list.sort(a)
    return [a[i+1] - a[i] for i in range(len(a) - 1)]

## Generate automata


def generateAutomata(timeStepNumber,size,r) :
    seed = generateSeed(size,0.05)
    rule = generateRandomRule(r)

    score = [seed]

    for t in range(timeStepNumber) :
        seed_plus =  [rule[tuple(seed[j+k - (j+k)//size * size] for k in range(-r,r+1))] for j in range(size) ]
        score.append(seed_plus)
        seed = seed_plus

    return(score)

## Visualization function

def plotAutomata(score) :
    sns.heatmap(score)
    plt.show()


""" Musical Part """

## Musical parameters

majorScaleInterval = [0,2,4,5,7,9,11] #Defines a Major scale
minorScaleInterval = [0,2,3,5,7,9,10] #Defines a Minor scale
chromaticScaleInterval = list(range(12))

def createRandomRythm(score_length) :
    track_rythm = []
    for b in range(score_length//8) :
        track_rythm += random_sum_to(32,8)
    track_rythm += random_sum_to(32,score_length%8)

    return(track_rythm)





## Convert Score to midi

def midiConverter(interval,score,height,root_note) :
    """
    Convert automata output into midi by specifying the scale, the root note and the amplitude of the melody (size of the window)
    """
    scale = [ root_note + (i//len(interval))*12 +interval[i - i//len(interval)*len(interval)]  for i in range(height) ]

    score = np.array(score)
    score = score[:,len(score[0])//2-height//2:len(score[0])//2+height//2]*scale # MIDI note number
    track_rythm = createRandomRythm(len(score))
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 150   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                        # automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, c in enumerate(score):
        for pitch in score[i] :
            if pitch != 0 :
                MyMIDI.addNote(track, channel, pitch, time + np.sum(track_rythm[:i])/4, track_rythm[i]/4, volume)

    with open("test.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

    sns.heatmap(score)
    plt.show()

def midiConverter2(interval,score,height,root_note) :
    scale = [ root_note + (i//len(interval))*12 +interval[i - i//len(interval)*len(interval)]  for i in range(height) ]

    score = np.array(score)
    score = score[:,len(score[0])//2-height//2:len(score[0])//2+height//2]*scale # MIDI note number
    track_rythm = createRandomRythm(len(score))
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 150   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                        # automatically)
    MyMIDI.addTempo(track, time, tempo)

    score = score.transpose()

    for note in score :
        note_duration = []
        for t in range(len(note)) :
            d = 0
            if note[t] == note[t+1] :
                d+=1
            # else :
            #     if note[t]



    with open("test.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

    sns.heatmap(score)
    plt.show()


def midi3statesConverter(interval,score,height,root_note) :
    """
    Function that creates a midi with 2 tracks using 3 states in Automata
    """

    scale = [ root_note + (i//len(interval))*12 +interval[i - i//len(interval)*len(interval)]  for i in range(height) ]

    score = np.array(score)
    score = score[:,len(score[0])//2-height//2:len(score[0])//2+height//2] # MIDI note number
    track1 = score//2 * scale
    track2 = (score - (score//2)* 2)*scale
    track1_rythm = createRandomRythm(len(score))
    track2_rythm = createRandomRythm(len(score))

    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 150   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(2)  # One track, defaults to format 1 (tempo track is created
                        # automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, c in enumerate(score):
        for p in range(len(score[i])) :
            if track1[i][p] != 0 :
                MyMIDI.addNote(0, channel,track1[i][p] , time + np.sum(track1_rythm[:i])/4, track1_rythm[i]/4, volume)
            if track2[i][p] != 0 :
                MyMIDI.addNote(1, channel,track2[i][p], time + np.sum(track2_rythm[:i])/4, track2_rythm[i]/4, volume)

    with open("test.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

if __name__ == '__main__':

    midi3statesConverter

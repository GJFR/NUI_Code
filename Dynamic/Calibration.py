'''
Created on 9-dec.-2013

@author: Kevin & Gertjan
'''

import IOFunctions
import DynamicSax
import Visualize
import threading
import queue
import time

if __name__ == '__main__':
    pass

MIN_SEQ_LENGTH = 100
MAX_SEQ_LENGTH = 150
WORD_LENGTH = 10
ALPHABET_SIZE = 10
COLLISION_THRESHOLD = 7
RANGE = 2
VALUE_A = 0.8
X = 5

def calibrate(directions):
    tijd = time.time()
    communicationGroups = queue.Queue()
    semaphore = threading.Semaphore(0)
    thread = threading.Thread(target=IOFunctions.IOCalibration, args=(communicationGroups, MIN_SEQ_LENGTH, MAX_SEQ_LENGTH, semaphore))
    thread.start()
    dts = DynamicSax.DynamicTimeSeq(MIN_SEQ_LENGTH, MAX_SEQ_LENGTH, WORD_LENGTH, ALPHABET_SIZE, COLLISION_THRESHOLD, RANGE)
    tijd = checkpoint("Init: ", tijd)
    while (dts.getNumberOfGroups() < 3):
        semaphore.acquire()
        dts.addSequenceGroup(nextGroup(communicationGroups))
        tijd = checkpoint("Group is done: ", tijd)
    motifs = dts.getMotifs()
    tijd = checkpoint("Get all motifs: ", tijd)
    dts.removeCloseMatches(motifs)
    tijd = checkpoint("Remove close matches: ", tijd)
    motif,matches = dts.getBestMotif(motifs)
    tijd = checkpoint("Get best motifs: ", tijd)
    IOFunctions.dataPlot(motif, matches)
    

def nextGroup(queue):
    return queue.get()

def checkpoint(message, previousTime):
    tijd = time.time()
    print (message + str(tijd - previousTime))
    return tijd
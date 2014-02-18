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

WORD_LENGTH = 10
ALPHABET_SIZE = 10
COLLISION_THRESHOLD = 7
RANGE = 2

def run(directions, allLengths):
    labels = {}
    for direction in directions:
        labels[direction] = calibrate(direction, allLengths)
    return labels

def calibrate(direction, allLengths):
    tijd = time.time()
    communicationGroups = queue.Queue()
    semaphore = threading.Semaphore(0)
    thread = threading.Thread(target=IOFunctions.IOCalibration, args=(communicationGroups, allLengths, semaphore, direction))
    thread.start()
    dts = DynamicSax.DynamicTimeSeq(WORD_LENGTH, ALPHABET_SIZE, COLLISION_THRESHOLD, RANGE)
    tijd = checkpoint("Init: ", tijd)
    while (dts.getNumberOfGroups() < 3):
        semaphore.acquire()
        dts.addSequenceGroup(nextGroup(communicationGroups))
        tijd = checkpoint("Group is done: ", tijd)
    dts.calculateMotifs()
    tijd = checkpoint("Get all motifs: ", tijd)
    dts.removeCloseMatches()
    tijd = checkpoint("Remove close matches: ", tijd)
    bestMotifs = dts.getBestMotifs(2)
    orderedBestMotifs = dts.orderMotifs(bestMotifs)
    tijd = checkpoint("Get best motifs: ", tijd)
    for motif in orderedBestMotifs:
        threadPlot = threading.Thread(target=IOFunctions.dataPlot, args=(motif, dts.getMotifs()[motif], direction))
        threadPlot.start()
        #IOFunctions.dataPlot(motif, dts.getMotifs()[motif], direction)
    return orderedBestMotifs

def nextGroup(queue):
    return queue.get()

def checkpoint(message, previousTime):
    tijd = time.time()
    print (message + str(tijd - previousTime))
    return tijd

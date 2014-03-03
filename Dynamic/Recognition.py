'''
Created on 9-dec.-2013

@author: Kevin & Gertjan
'''
import SeqChecker
import IOFunctions
import threading
import queue
import time

WORD_LENGTH = 10
ALPHABET_SIZE = 10
COLLISION_THRESHOLD = 7
RANGE = 2

if __name__ == '__main__':
    pass

def recognize(labels, minSeqLength, allLengths):
    tijd = time.time()
    seqChecker = SeqChecker.SeqChecker(labels, WORD_LENGTH, ALPHABET_SIZE, COLLISION_THRESHOLD, RANGE)
    semaphore = threading.Semaphore(0)
    communicationSequences = queue.Queue()
    thread = threading.Thread(target=IOFunctions.IORecognition, args=(communicationSequences, minSeqLength, allLengths, semaphore))
    thread.start()
    labeledMatches = {}
    for label in labels:
        labeledMatches[label] = []
    tijd = checkpoint("Init: ", tijd)
    for i in range(3000 * 11):
        semaphore.acquire()
        nextSeq = nextSequence(communicationSequences)
        label = seqChecker.checkSequence(nextSeq)
        if (label is not None):
            labeledMatches[label] = nextSeq
            print(str(nextSeq) + ": " + label)
    
def nextSequence(queue):
    return queue.get()
    
def checkpoint(message, previousTime):
    tijd = time.time()
    print (message + str(tijd - previousTime))
    return tijd

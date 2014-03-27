import eyetracking2
import TimeSequence
import ThresholdSolution
import PatternSolution
import Visualize
import DataWindow
import numpy as np
from time import sleep
import queue
import threading

inputQueue = queue.Queue()
queueSemaphore = threading.Semaphore(10000)
queueAccessLock = threading.Lock()

THRESHOLD_CALIBRATION_LENGTH = 150
ALPHABET_SIZE = 8
VALUES_PER_LETTER = 15

directionThresholds = {"Left" : 0.5, "Right" : 0.5}
minimalThresholdHits = 7

def runT():
    #thread = threading.Thread(target=eyetracking2.run, args=(inputQueue,queueSemaphore,queueAccessLock))
    #thread.start()

    distribution = thresholdsCalibration()
    print(distribution)
    thresholdsRecognition(distribution)


# TODO semaphore in plaats van lock
def thresholdsCalibration():
    data = eyetracking2.run2(THRESHOLD_CALIBRATION_LENGTH)
    timeSeq = TimeSequence.TimeSequence(data)
    timeSeq.filter()
    timeSeq.makeSaxWord(ALPHABET_SIZE, VALUES_PER_LETTER)

    directionThresholds["Left"] = timeSeq.getMinimalValue() * directionThresholds["Left"]
    directionThresholds["Right"] = timeSeq.getMaximalValue() * directionThresholds["Right"]
    
    print("Left threshold: " + str(directionThresholds["Left"]))
    print("Right threshold: " + str(directionThresholds["Right"]))
    
    thresholdSol = ThresholdSolution.ThresholdSolution(directionThresholds, minimalThresholdHits)
    #thresholdSol.processTimeSequenceCalibration(timeSeq)

    Visualize.plot_data_saxString(timeSeq,ALPHABET_SIZE,VALUES_PER_LETTER)

    answer = input("Ben je tevreden met de resultaten? (y/n)")
    if answer == "y":
        return (timeSeq.getDistribution())
    else:
        return thresholdsCalibration()

def thresholdsRecognition(distribution):
    thresholdSol = ThresholdSolution.ThresholdSolution(directionThresholds, minimalThresholdHits)
    dataWindow = DataWindow.DataWindow(distribution)
    thread = threading.Thread(target=eyetracking2.run, args=(inputQueue,queueSemaphore,queueAccessLock,dataWindow))
    thread.start()
    
    for i in range(100):
        letterPart = inputQueue.get(True)
        dataWindow.addData(letterPart)
        lastLetter = dataWindow.getLastLetter()
    print("End of data window fill.")
    while(True):
        letterPart = inputQueue.get(True)
        dataWindow.addData(letterPart)
        lastLetter = dataWindow.getLastValue()
        #print(lastLetter)
        if(thresholdSol.processTimeSequenceRecognition(lastLetter)):
            1==1
            dataWindow.vlakAf()


###########################################################################################
###########################################################################################
###########################################################################################
PATTERN_CALIBRATION_LENGTH = 40
P_ALPHABET_SIZE = 8
P_VALUES_PER_LETTER = 10
P_MAX_MATCHING_DISTANCE = 3


def runP():
    patternCalibration()

def patternCalibration():
    dataDict = {"Left" : [],"Right" : []}
    for i in range(3):
        for direction in dataDict:
            print(direction)
            sleep(0.5)
            dataDict[direction].append(eyetracking2.run2(PATTERN_CALIBRATION_LENGTH))
    
    patternSol = PatternSolution.PatternSolution(dataDict,P_ALPHABET_SIZE,P_VALUES_PER_LETTER, P_MAX_MATCHING_DISTANCE)
   
def patternRecognition(distribution):
   patternSol = PatternSolution.PatternSolution(P_MAX_MATCHING_DISTANCE, P_ALPHABET_SIZE, P_VALUES_PER_LETTER)
   dataWindow = DataWindow.DataWindow(distribution)

   thread = threading.Thread(target=eyetracking2.run, args=(inputQueue,queueSemaphore,queueAccessLock,dataWindow))
   thread.start()

   for i in range(100):
        letterPart = inputQueue.get(True)
        dataWindow.addData(letterPart)
        lastLetter = dataWindow.getLastLetter()
   print("End of data window fill.")

   while(True):
        letterPart = inputQueue.get(True)
        dataWindow.addData(letterPart)
        lastLetter = dataWindow.getLastValue()
        #print(lastLetter)
        if(patternSol.processTimeSequenceRecognition(lastLetter)):
            1==1
            dataWindow.vlakAf()

if __name__ == '__main__':
    runP()
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
AANTAL_LETTERS = 8
WAARDES_PER_LETTER = 15

directionThresholds = {"Left" : 0.5, "Right" : 0.5}
minimalThresholdHits = 7

def runT():
    #thread = threading.Thread(target=eyetracking2.run, args=(inputQueue,queueSemaphore,queueAccessLock))
    #thread.start()

    thresholds = thresholdsCalibration()
    print(thresholds)
    thresholdsRecognition(thresholds)


# TODO semaphore in plaats van lock
def thresholdsCalibration():
    data = eyetracking2.run2(THRESHOLD_CALIBRATION_LENGTH)
    timeSeq = TimeSequence.TimeSequence(data)
    timeSeq.filter()
    timeSeq.makeSaxWord(AANTAL_LETTERS, WAARDES_PER_LETTER)

    directionThresholds["Left"] = timeSeq.getMinimalValue() * directionThresholds["Left"]
    directionThresholds["Right"] = timeSeq.getMaximalValue() * directionThresholds["Right"]
    
    print("Left threshold: " + str(directionThresholds["Left"]))
    print("Right threshold: " + str(directionThresholds["Right"]))
    
    thresholdSol = ThresholdSolution.ThresholdSolution(directionThresholds, minimalThresholdHits)
    #thresholdSol.processTimeSequenceCalibration(timeSeq)

    Visualize.plot_data_saxString(timeSeq,AANTAL_LETTERS,WAARDES_PER_LETTER)

    answer = input("Ben je tevreden met de resultaten? (y/n)")
    if answer == "y":
        return (timeSeq.getThresholds())
    else:
        return thresholdsCalibration()

def thresholdsRecognition(thresholds):
    thresholdSol = ThresholdSolution.ThresholdSolution(directionThresholds, minimalThresholdHits)
    dataWindow = DataWindow.DataWindow(thresholds)
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
PATTERN_CALIBRATION_LENGTH = 50
P_AANTAL_LETTERS = 8
P_WAARDES_PER_LETTER = 10
P_MAX_MATCHING_DISTANCE = 3


def runP():
    patternCalibration()

P_MAX_MATCHING_DISTANCE
def patternCalibration():
    dataDict = {"Left" : [],"Right" : []}
    print("links")
    sleep(0.5)
    dataDict["Left"].append(eyetracking2.run2(PATTERN_CALIBRATION_LENGTH))
    print("Right")
    sleep(0.5)
    dataDict["Right"].append(eyetracking2.run2(PATTERN_CALIBRATION_LENGTH))
    print("links")
    sleep(0.5)
    dataDict["Left"].append(eyetracking2.run2(PATTERN_CALIBRATION_LENGTH))
    print("Right")
    sleep(0.5)
    dataDict["Right"].append(eyetracking2.run2(PATTERN_CALIBRATION_LENGTH))
    print("links")
    sleep(0.5)
    dataDict["Left"].append(eyetracking2.run2(PATTERN_CALIBRATION_LENGTH))
    print("Right")
    sleep(0.5)
    dataDict["Right"].append(eyetracking2.run2(PATTERN_CALIBRATION_LENGTH))
    
    patternSol = PatternSolution.PatternSolution(P_MAX_MATCHING_DISTANCE,P_AANTAL_LETTERS,P_WAARDES_PER_LETTER)
    patternSol.processTimeSequenceCalibration(dataDict)
    

if __name__ == '__main__':
    runP()
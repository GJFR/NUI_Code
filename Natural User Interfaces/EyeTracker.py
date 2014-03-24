import eyetracking2
import TimeSequence
import ThresholdSolution
import Visualize
import DataWindow
import numpy as np

import queue
import threading

inputQueue = queue.Queue()
queueSemaphore = threading.Semaphore(0)
queueAccessLock = threading.Lock()

calibrationLength = 150
aantalLetters = 8
waardesPerLetter = 15

directionThresholds = {"Left" : 0.5, "Right" : 0.5}
minimalThresholdHits = 7

def run():
    #thread = threading.Thread(target=eyetracking2.run, args=(inputQueue,queueSemaphore,queueAccessLock))
    #thread.start()

    thresholds = thresholdsCalibration()
    print(thresholds)
    thresholdsRecognition(thresholds)


# TODO semaphore in plaats van lock
def thresholdsCalibration():
    data = []
    data = eyetracking2.run2(data, calibrationLength)
    timeSeq = TimeSequence.TimeSequence(data)
    timeSeq.filter()
    timeSeq.makeSaxWord(aantalLetters, waardesPerLetter)

    directionThresholds["Left"] = timeSeq.getMinimalValue() * directionThresholds["Left"]
    directionThresholds["Right"] = timeSeq.getMaximalValue() * directionThresholds["Right"]
    
    print("Left threshold: " + str(directionThresholds["Left"]))
    print("Right threshold: " + str(directionThresholds["Right"]))
    
    thresholdSol = ThresholdSolution.ThresholdSolution(directionThresholds, minimalThresholdHits)
    #thresholdSol.processTimeSequenceCalibration(timeSeq)

    Visualize.plot_data_saxString(timeSeq,aantalLetters,waardesPerLetter)

    answer = input("Ben je tevreden met de resultaten? (y/n)")
    if answer == "y":
        return (timeSeq.getThresholds())
    else:
        return thresholdsCalibration()

def thresholdsRecognition(thresholds):
    thresholdSol = ThresholdSolution.ThresholdSolution(directionThresholds, minimalThresholdHits)
    queueSemaphore = threading.Semaphore(10000)
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

if __name__ == '__main__':
    run()
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

calibrationLength = 100
aantalLetters = 8
waardesPerLetter = 15

directionThresholds = {"Left" : "c", "Right" : "f"}
minimalThresholdHits = 14

def run():
    thread = threading.Thread(target=eyetracking2.run, args=(inputQueue,queueSemaphore,queueAccessLock))
    thread.start()

    thresholds = thresholdsCalibration()


# TODO semaphore in plaats van lock
def thresholdsCalibration():
    data = []
    for i in range(10):
        queueSemaphore.release()
    for i in range(int(calibrationLength / 10)):
        # queue van paren
        dataPart_A, dataPart_B = inputQueue.get(True)
        # extend eigenlijk
        data.extend(dataPart_B)
    while not inputQueue.empty():
        inputQueue.get()
    timeSeq = TimeSequence.TimeSequence(data, aantalLetters, waardesPerLetter)
    timeSeq.filter()
    sortedMatrix = sorted(timeSeq.getMatrix())
    timeSeq.makeThresholds(sortedMatrix)
    timeSeq.makeSaxString(sortedMatrix)

    thresholdSol = ThresholdSolution.ThresholdSolution(directionThresholds, minimalThresholdHits)
    thresholdSol.processTimeSequenceCalibration(timeSeq)

    Visualize.plot_data_saxString(timeSeq,aantalLetters,waardesPerLetter)

    answer = raw_input("Ben je tevreden met de resultaten? (y/n)")
    if answer == "y":
        return (timeSeq.getThresholds())
    else:
        return thresholdsCalibration()

def thresholdsRecognition(thresholds):
    thesholdSol = ThresholdSolution.ThresholdSolution(directionsThresholds, minimalThresholdHits)
    dataWindow = DataWindow.DataWindow(thesholds)
    queueLock.release()
    while(True):
        letterPart = inputQueue.get(True)
        dataWindow.addData(letterPart)
        lastLetter = dataWindow.getLastLetter()
        thresholdSol.processTimeSequenceRecognition(lastLetter)

if __name__ == '__main__':
    run()
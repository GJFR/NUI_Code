import eyetracking2
import TimeSequence
import ThresholdSolution
import Visualize
import DataWindow

import queue
import threading

inputQueue = queue.Queue()
queueLock = threading.Lock()

calibrationLength = 1000
aantalLetters = 8
waardesPerLetters = 15

directionThresholds = {"Left" : "c", "Right" : "f"}
minimalThresholdHits = 14

def run():
    queueLock.acquire()
    thread = threading.Thread(target=eyetracking2.run, args=(inputQueue,queueLock,))
    thread.start()

    thresholds = thresholdsCalibration()


def thresholdsCalibration():
    queueLock.release()
    data = []
    for i in range(int(calibrationLength / 10)):
        dataPart = inputQueue.get(True)
        data.extend(dataPart)
    queueLock.acquire(True)
    while not inputQueue.Empty:
        inputQueue.get()
    timeSeq = TimeSequence.TimeSequence(data, aantalLetters, waardesPerLetter)
    timeSeq.filter()
    sortedMatrix = sorted(timeSeq.getMatrix())
    timeSeq.makeThresholds(sortedMatrix)
    timeSeq.makeSaxString(sortedMatrix)

    thresholdSol = ThresholdSolution.ThresholdSolution(timeSeq, directionThresholds, minimalThresholdHits)
    thresholdSol.processTimeSequence()

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
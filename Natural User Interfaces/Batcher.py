import Visualize
import TimeSequence
import ThresholdSolution
import PatternSolution
import DataWindow
import os
import csv
from time import sleep
import threading
from scipy.signal import filtfilt, butter
import matplotlib.pyplot as plt
import numpy as np

class Batcher(object):

    def __init__(self, alphabetSize, valuesPerLetter):
        self.alphabetSize = alphabetSize
        self.valuesPerLetter = valuesPerLetter
        self.eog = np.zeros(1000)

    def getCalibrationVector(self):
        return self.calibrationVector

    """Adds None to the end of the input queue"""
    def fillQueue(self, inputQueue, dataWindow):
        thread = threading.Thread(target=self.plot_data, args=(dataWindow,))
        thread.start()
        for i in range(0,len(self.recognitionVector),10):
            newValues = self.recognitionVector[i:i+10]
            inputQueue.put(newValues)
            self.eog[0:990] = self.eog[10:1000]
            self.eog[990:1000] = newValues
            sleep(0.08)
        inputQueue.put(None)

    def setCalibrationData(self, index, path):
        self.calibrationVector = self.readData(path, 23)[index:index + 2200]

    def setRecognitionData(self, path):
        self.recognitionVector = self.readData(path, 23)

    def runThresholds(self):
        calibrationTS = TimeSequence.TimeSequence(self.calibrationVector)
        calibrationTS.filter()
        sortedMatrix = sorted(calibrationTS.getVector())
        calibrationTS.makeSaxWord(self.alphabetSize, self.valuesPerLetter)

        thresholdSol = ThresholdSolution.ThresholdSolution(14, 50)

        """Uitvoeren Calibration"""
        thresholdSol.processTimeSequenceCalibration(calibrationTS)
        Visualize.plot_data_saxString(calibrationTS, self.alphabetSize, self.valuesPerLetter)

    def readData(self, relativePath, nbr):
        try:
            # Eclipse
            path = (os.getcwd()[:len(os.getcwd())-nbr])
            with open(path + "\\" + relativePath) as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    return [float(i) for i in row]
        except FileNotFoundError:
            # Visual Studio
            path = (os.getcwd()[:len(os.getcwd())])
            with open(path + "\\" + relativePath) as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    return [float(i) for i in row]

    def plot_data(self,dataWindow):

        print("Init plotting")
        b, a = butter(2, 0.0001, 'high')
        #b, a = butter(2, 0.5, 'high')

        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        line1, = ax1.plot(dataWindow.filt_data)
        line2, = ax2.plot(self.eog)
        fig.show()

        print("Start plotting")

        #while True:
        for t in range(int(len(self.recognitionVector)/10) + 1):

            #print("Filtering")
            eog_filt = filtfilt(b, a, self.eog)

            #print("Plotting")
            line1.set_ydata(dataWindow.filt_data)
            #ax1.set_ylim((min(eog1_filt), max(eog1_filt)))
            ax1.set_ylim(-50000,50000)
            line2.set_ydata(eog_filt)
            #ax2.set_ylim((min(eog2_filt), max(eog2_filt)))
            ax2.set_ylim(-50000,50000)
            fig.canvas.draw()
            fig.show()

            sleep(.5)

        print("Plotting ended")

if __name__ == '__main__':
    MAX_MATCHING_DISTANCE = 25
    ALPHABET_SIZE = 8
    VALUES_PER_LETTER = 15


    calibrationPath = 'Data2\\test24_B.csv'
    calibrationIndex = 250
    recognitionPath = 'Data2\\test24_B.csv'

    batcher = Batcher(ALPHABET_SIZE, VALUES_PER_LETTER)
    batcher.setCalibrationData(calibrationIndex, calibrationPath)
    batcher.runThresholds()

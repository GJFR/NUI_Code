import numpy as np
from scipy.signal import filtfilt, butter

class DataWindow(object):
    """description of class"""

    def __init__(self, thresholds):
        self.thresholds = thresholds
        self.data = np.zeros(1000)
        self.filt_data = np.zeros(1000)
        self.allLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def addData(self, dataPart):
        self.data[0:990] = self.data[10:1000]
        self.data[990:1000] = dataPart
        self.makeFiltered()

    def makeFiltered(self):
        filtered = np.zeros(len(self.data))
        b1, a1 = butter(1, 0.0003, 'lowpass')
        filtered = filtfilt(b1, a1, self.data)
        self.filt_data = self.data - filtered
        # Nog een lowpass filter

    def getLastLetter(self):
        letter = ""
        lastPart = self.data[990:1000]
        average = sum(lastPart) / len(lastPart)
        for j in range(1,len(self.thresholds)):
            if average < self.thresholds[j]:
                letter = self.allLetters[j-1]
                break
        else:
            letter = self.allLetters[len(self.thresholds) - 1]
        return letter
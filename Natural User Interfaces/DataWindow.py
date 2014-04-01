import numpy as np
from scipy.signal import filtfilt, butter

class DataWindow(object):
    """description of class"""

    def __init__(self):
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
        filtered = self.data - filtered
        b2, a2 = butter(1, 0.05, 'lowpass')
        self.filt_data = filtfilt(b2, a2, filtered)

    def getLastValue(self):
        letter = ""
        lastPart = self.filt_data[990:1000]
        return sum(lastPart) / len(lastPart)  
          
    def getLastLetter(self, distribution):
        letter = ""
        lastPart = self.filt_data[990:1000]
        average = sum(lastPart) / len(lastPart)
        for j in range(1,len(distribution)):
            if average < self.thresholds[j]:
                letter = self.allLetters[j-1]
                break
        else:
            letter = self.allLetters[len(distribution) - 1]
        return letter
    
    def vlakAf(self):
        secondLastPart = self.data[0:990]
        average = sum(secondLastPart) / len(secondLastPart)
        self.data[990:1000] = [average] * 10
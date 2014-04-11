import numpy as np
from scipy.signal import filtfilt, butter
import SaxWord

class DataWindow(object):
    """description of class"""

    def __init__(self):
        self.bufferSize = 1000;
        self.data = np.zeros(self.bufferSize)
        self.filt_data = np.zeros(self.bufferSize)
        self.allLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def addData(self, dataPart):
        self.data[0 : self.bufferSize - 10] = self.data[10 : self.bufferSize]
        self.data[self.bufferSize - 10 : self.bufferSize] = dataPart
        self.makeFiltered()

    def makeFiltered(self):
        filtered = np.zeros(len(self.data))
        b1, a1 = butter(1, 0.0003, 'lowpass')
        filtered = filtfilt(b1, a1, self.data)
        filtered = self.data - filtered
        b2, a2 = butter(1, 0.05, 'lowpass')
        self.filt_data = filtfilt(b2, a2, filtered)

    def getLastSequence(self, size):
        if (size > self.bufferSize):
            raise AttributeError('The size is too large')
        return self.filt_data[self.bufferSize - size : self.bufferSize]

    def getLastValue(self):
        letter = ""
        lastPart = self.filt_data[self.bufferSize - 10 : self.bufferSize]
        return sum(lastPart) / len(lastPart)  
          
    def getLastLetter(self, distribution):
        letter = ""
        lastPart = self.filt_data[self.bufferSize - 10 : self.bufferSize]
        average = sum(lastPart) / len(lastPart)
        for j in range(1,len(distribution)):
            if average < self.distribution[j]:
                letter = self.allLetters[j-1]
                break
        else:
            letter = self.allLetters[len(distribution) - 1]
        return letter
    
    def getLastSaxWord(self, length, alphabetSize, valuesPerLetter, distribution=None, letterWaarden=None):
        vector = self.filt_data[self.bufferSize - length: self.bufferSize]
        return SaxWord.SaxWord(vector, alphabetSize, valuesPerLetter, distribution, letterWaarden)
    
    def flatten(self):
        secondLastPart = self.data[0 : self.bufferSize - 10]
        average = sum(secondLastPart) / len(secondLastPart)
        self.data[self.bufferSize - 10 : self.bufferSize] = [average] * 10
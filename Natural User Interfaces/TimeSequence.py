'''
Created on 8-nov.-2013

@author: Gertjan & Kevin
'''


import numpy as np
from scipy.signal import filtfilt, butter
import os
import csv
import math

import SaxWord

class TimeSequence(object):
    """
    TimeSequence objects hold data that is used to determine the viewing direction(s).
    """

    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, vector):
        # A TimeSequence instance doesn't necessarily have a saxWord.
        self.saxWord = None
        self.setVector(vector)
        

    def getThresholds(self):
        return self.getSaxWord().getThresholds()

    def getSaxWord(self):
        return self.saxWord
    
    def getLetterWaarden(self):
        return self.getSaxWord().getLetterWaarden()

    def setVector(self, vector):
        self.vector = vector
        
    def getVector(self):
        return self.vector
    
    def getMinimalValue(self):
        return min(self.getVector())
    
    def getMaximalValue(self):
        return max(self.getVector())
        
    def normalize(self):
        """
        Normalizes this time sequence.
        """
        mean = sum(self.vector)/len(self.vector)
        nVector = self.vector
        nVector = [(x-mean) for x in nVector]
        '''nMatrix = self.__matrix - mean'''
        nVector = [(x/np.absolute(nVector).max()) for x in nVector]
        '''self.__matrix = nMatrix/abs(nMatrix).max()'''
        self.vector = nVector
        
    def filter(self):
        """
        Filters this time sequence.
        """
        eog_filt1 = np.zeros(len(self.vector))
        b1, a1 = butter(1, 0.0003, 'lowpass')
        eog_filt1 = filtfilt(b1, a1, self.vector)
        matrix2 = (self.getVector() - eog_filt1)
        b2, a2 = butter(1, 0.05, 'lowpass')
        eogfilt2 = filtfilt(b2, a2, matrix2)
        self.setVector(eogfilt2)

    def extend(self, other):
        """
        Extends this time sequence with another time sequence and returns the result as a new time sequence.
        Parameters:
            other   - the other time sequence
        """
        appendedMatrix = self.getVector().copy()
        otherMatrix = other.getMatrix().copy()
        appendedMatrix.extend(otherMatrix)
        return TimeSequence(appendedMatrix, self.aantalLetters, self.waardesPerLetter)
        
    def makeSaxWord(self, alphabetSize, valuesPerLetter):
        """
        Makes a the sax word of this time sequence.
        Parameters:
            alphabetSize    - the number of letters that is used to construct the sax word
            valuesPerLetter - the number of values that is given to a letter
        """
        self.saxWord = SaxWord.SaxWord(self.vector, alphabetSize, valuesPerLetter)

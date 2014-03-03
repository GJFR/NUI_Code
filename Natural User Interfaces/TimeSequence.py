'''
Created on 8-nov.-2013

@author: Gertjan & Kevin
'''


import numpy as np
from scipy.signal import filtfilt, butter
import os
import csv
import math

class TimeSequence(object):
    '''
    classdocs
    '''
    thresholds = []
    saxString = ""
    letterWaarden = {}
    allLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, matrix, aantalLetters, waardesPerLetter):
        '''
        Constructor
        '''
        self.aantalLetters = aantalLetters
        self.waardesPerLetter = waardesPerLetter
        self.setMatrix(matrix)
        sortedMatrix = sorted(self.getMatrix())
        self.makeThresholds(sortedMatrix)
        self.makeSaxString(sortedMatrix)

    def getThresholds(self):
        return self.thresholds

    def getSaxString(self):
        return self.saxString
    
    def getLetterWaarden(self):
        return self.letterWaarden

    def setMatrix(self,matrix):
        self.matrix = matrix
        
    def getMatrix(self):
        return self.matrix
        
    def normalize(self):
        mean = sum(self.matrix)/len(self.matrix)
        nMatrix = self.matrix
        nMatrix = [(x-mean) for x in nMatrix]
        '''nMatrix = self.__matrix - mean'''
        nMatrix = [(x/np.absolute(nMatrix).max()) for x in nMatrix]
        '''self.__matrix = nMatrix/abs(nMatrix).max()'''
        self.matrix = nMatrix
        
    def filter(self):
        eog_filt1 = np.zeros(len(self.matrix))
        '''4, 0.016'''
        b1, a1 = butter(1, 0.0003, 'lowpass')
        b2, a2 = butter(4, 0.00005, 'highpass')
        #eog_filt1 = filtfilt(b2, a2, self.__matrix)
        eog_filt2 = filtfilt(b1, a1, self.matrix)   
        self.setMatrix(eog_filt2)

    def extend(self, other):
        appendedMatrix = self.getMatrix().copy()
        otherMatrix = other.getMatrix().copy()
        appendedMatrix.extend(otherMatrix)
        return TimeSequence(appendedMatrix, self.aantalLetters, self.waardesPerLetter)
        
    def makeSaxString(self, sortedMatrix):
        positie = 0
        thresholds = self.getThresholds()
        for index in range(0,len(self.getMatrix()) - self.waardesPerLetter,self.waardesPerLetter):
            totalOfTen = 0
            for j in range(self.waardesPerLetter):
                totalOfTen = totalOfTen + self.getMatrix()[index+j]
            average = totalOfTen / self.waardesPerLetter
            for j in range(1,self.aantalLetters+1):
                if average < self.thresholds[j]:
                    self.saxString = self.saxString + self.allLetters[j - 1]
                    break
            else:
                self.saxString = self.saxString + self.allLetters[self.aantalLetters-1]
        self.makeLetterwaarden(sortedMatrix)

    def makeThresholds(self, sortedMatrix):
        self.thresholds.append(sortedMatrix[0])
        for index in range(1,self.aantalLetters + 1):
            positie = math.floor(index * len(sortedMatrix)/self.aantalLetters)-1
            self.thresholds.append(sortedMatrix[positie])
        
    def makeLetterwaarden(self, sortedMatrix):
        posities = [0]
        for index in range(1,self.aantalLetters+1):
            posities.append(math.floor(index * len(sortedMatrix)/self.aantalLetters)-1)
        for index in range(len(posities) - 1):
            total = 0
            for pos in range(posities[index], posities[index+1]):
                total = total + sortedMatrix[pos]
            mean = total / (posities[index+1] - posities[index])
            self.letterWaarden[self.allLetters[index]] = mean
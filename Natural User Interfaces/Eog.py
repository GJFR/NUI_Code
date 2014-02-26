'''
Created on 8-nov.-2013

@author: Gertjan & Kevin
'''


import numpy as np
from scipy.signal import filtfilt, butter
import os
import csv
import math

class Eog(object):
    '''
    classdocs
    '''
    thresholds = []
    saxString = ""
    letterWaarden = {}

    def __init__(self, relativePath, nbr):
        '''
        Constructor
        '''
        self.setMatrix(self.readData(relativePath, nbr))
        self.setAnnotations([])

    def getThresholds(self):
        return self.thresholds


    def getSaxString(self):
        return self.saxString
    
    def getLetterWaarden(self):
        return self.letterWaarden

    def setMatrix(self,matrix):
        self.__matrix = matrix
        
    def getMatrix(self):
        return self.__matrix
    
    def setAnnotations(self,annotations):
        self.__annotations = annotations
        
    def addAnnotation(self,annotation):
        self.__annotations.append(annotation)
        
    def getAnnotations(self):
        return self.__annotations
        
    def normalize(self):
        mean = sum(self.__matrix)/len(self.__matrix)
        nMatrix = self.__matrix
        nMatrix = [(x-mean) for x in nMatrix]
        '''nMatrix = self.__matrix - mean'''
        nMatrix = [(x/np.absolute(nMatrix).max()) for x in nMatrix]
        '''self.__matrix = nMatrix/abs(nMatrix).max()'''
        self.__matrix = nMatrix
        
    def filter(self):
        
        eog_filt1 = np.zeros(len(self.__matrix))
        '''4, 0.016'''
        b1, a1 = butter(1, 0.01, 'lowpass')
        b2, a2 = butter(4, 0.001, 'highpass')
        eog_filt1 = filtfilt(b2, a2, self.__matrix)
        eog_filt2 = filtfilt(b1, a1, eog_filt1)   
        self.setMatrix(eog_filt1)
    
    def readData(self, relativePath, nbr):
        path = (os.getcwd()[:len(os.getcwd()) - nbr])

        with open(path + relativePath) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                return [float(i) for i in row]

    def append(self, other):
        appendedMatrix = self.getMatrix() + other.getMatrix()
        self.setMatrix(appendedMatrix)
        
    def makeSaxString(self,aantalLetters):
        sortedMatrix = sorted(self.getMatrix())
        lst = "abcdefghijklmnopqrstuvwxyz"
        positie = 0
        self.thresholds.append(sortedMatrix[0])
        for index in range(1,aantalLetters + 1):
            positie = math.floor(index * len(sortedMatrix)/aantalLetters)-1
            self.thresholds.append(sortedMatrix[positie])
        for index in range(0,len(self.getMatrix()),aantalLetters):
            totalOfTen = 0
            for j in range(aantalLetters):
                totalOfTen = totalOfTen + self.getMatrix()[index+j]
            average = totalOfTen / aantalLetters
            for j in range(1,aantalLetters-1):
                if average < self.thresholds[j]:
                    self.saxString = self.saxString + lst[j]
                    break
            else:
                self.saxString = self.saxString + lst[aantalLetters-1]
        
        for index in range(10):
            
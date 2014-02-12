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


    def __init__(self, relativePath, nbr):
        '''
        Constructor
        '''
        self.setMatrix(self.readData(relativePath, nbr))
        self.setAnnotations([])

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
        
        eog_filt = np.zeros(len(self.__matrix))
        '''4, 0.016'''
        b, a = butter(3, 0.032, 'low')
        eog_filt = filtfilt(b, a, self.__matrix)
        self.setMatrix(eog_filt)
    
    def readData(self, relativePath, nbr):
        path = (os.getcwd()[:len(os.getcwd()) - nbr])

        with open(path + relativePath) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                return [float(i) for i in row]
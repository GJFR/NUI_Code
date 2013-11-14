'''
Created on 14-nov.-2013

@author: Gertjan & Kevin
'''
import math
import numpy as np
import scipy.stats

class Sequence(object):
    '''
    classdocs
    '''
    x = scipy.stats.norm(0,1)
    lst = " abcdefghijklmnopqrstuvwxyz"

    def __init__(self,  timeSeq, start, length):
        '''
        Constructor
        '''
        self.timeSeq = timeSeq
        self.start = start
        self.length = length
        
    def getPoint(self, i):
        return self.timeSeq[self.start + i]
        
    def getAllPoints(self):
        return self.timeSeq[self.start: self.start + self.length]
        
    def getNormalized(self):
        nMatrix = self.getAllPoints()
        mean = sum(nMatrix)/self.length
        nMatrix = [(x-mean) for x in nMatrix]
        nMatrix = [(x/np.absolute(nMatrix).max()) for x in nMatrix]
        return NormSequence(self.timeSeq, self.start, self.length, nMatrix, self)
    
    def compareEuclDist(self, other):
        som = 0
        for i in range(self.length):
            som += (self.getPoint(i) - other.getPoint(i))**2
        return math.sqrt(som)
        
    def isNonTrivial(self, other):
        pass
    
    def getWord(self, woordLengte, alfabetGrootte):
        word = ""
        for i in range(woordLengte):
            total = 0
            for j in range(int((self.length/woordLengte) * (i - 1) + 1),int((self.length/woordLengte) * i) + 1):
                total += self.getPoint(j)
            value = (woordLengte/self.length) * total
            word += self.getLetter(value, alfabetGrootte)
        return word
    
    def getLetter(self, value, alfabetGrootte):
        letterWaarde = self.x.cdf(value) * alfabetGrootte
        for i in range(1,alfabetGrootte + 1):
            if letterWaarde < i :
                return self.lst[i]
        return ""
    
    def __str__(self):
        return str(self.start)
    
    def __repr__(self):
        return str(self.start)
    
class NormSequence(Sequence):
    
    def __init__(self,  timeSeq, start, length, normData, originalSeq):
        '''
        Constructor
        '''
        super().__init__(timeSeq, start, length)
        self.normData = normData
        self.originalSeq = originalSeq
        
    def getPoints(self, i):
        return self.normData[i]
    
    def getAllPoints(self):
        return self.normData
    
    def getOriginal(self):
        return self.originalSeq
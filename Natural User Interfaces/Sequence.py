'''
Created on 14-nov.-2013

@author: Gertjan
'''
import math
import numpy as np

class MyClass(object):
    '''
    classdocs
    '''


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
        return self.timeSeq[self.start, self.start + self.length]
        
    def getNormalized(self):
        nMatrix = self.getAllPoints()
        mean = sum(nMatrix)/self.length
        nMatrix = [(x-mean) for x in nMatrix]
        nMatrix = [(x/np.absolute(nMatrix).max()) for x in nMatrix]
        return nMatrix
    
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
                total += self.getPoint(i)
            waarde = (woordLengte/self.length) * total
            word += self.getLetter(waarde)
        return word
    
    def getLetter(self,alfabetGrootte):
        letterWaarde = self.x.cdf(waarde) * alfabetGrootte
        for i in range(1,self.alfabetGrootte + 1):
            if letterWaarde < i :
                return self.lst[i]
        return ""
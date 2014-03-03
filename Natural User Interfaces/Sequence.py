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

    def __init__(self,  timeSeq, start, length):
        '''
        Constructor
        '''
        self.timeSeq = timeSeq
        self.start = start
        self.length = length
        
    def getStart(self):
        return self.start
    
    def getLength(self):
        return self.length
        
    def getPoint(self, i):
        self.testIndex(i)
        return self.timeSeq[self.getStart() + i]
        
    def testIndex(self, i):
        if self.getLength() <= abs(i):
            raise IndexError
        
    def getAllPoints(self):
        return self.timeSeq[self.getStart(): self.getStart() + self.getLength()]
      
    '''Returns a new object of class NormSequence made with timeSeq and self'''  
    def getNormalized(self):
        return NormSequence(self.timeSeq, self)
    
    '''Calculates the Euclidean distance between 2 Sequences of the same length'''
    def compareEuclDist(self, other):
        som = 0
        for i in range(self.getLength()):
            p1 = self.getPoint(i)
            p2 = other.getPoint(i)
            som += (self.getPoint(i) - other.getPoint(i))**2
        return math.sqrt(som)
            
    def isNonTrivial(self, other):
        pass
    
    '''Returns the SAX-word of this sequence based on the woordLengte and alfabetGrootte'''

    
    def getWord(self, woordLengte, alfabetGrootte):
        self.timeSeq.get
        return word
        
    '''Returns the letter appropriate for the value based on alfabetGrootte'''
    def getLetter(self, value, alfabetGrootte):
        letterWaarde = self.x.cdf(value) * alfabetGrootte
        for i in range(1,alfabetGrootte + 1):
            if letterWaarde < i :
                return self.allLetters[i]
        return ""
    
    '''Returns the distance between the starting position of this and other sequence'''
    def getDistance(self, other):
        return abs(self.getStart() - other.getStart())
    
    def overlap(self,seq):
        if(self.getStart() + self.getLength() > seq.getStart() and self.getStart() <= seq.getStart()):
            return True
        elif(seq.getStart() + seq.getLength() > self.getStart() and seq.getStart() <= self.getStart()):
            return True
        return False
    
    '''override'''
    def __str__(self):
        return str(self.getStart()) + " (" + str(self.getLength()) + ")"
    
    '''override'''
    def __repr__(self):
        return str(self.getStart()) + " (" + str(self.getLength()) + ")"
    
class NormSequence(Sequence):
    
    def __init__(self,  timeSeq, originalSeq):
        '''
        Constructor
        '''
        super().__init__(timeSeq, originalSeq.getStart(), originalSeq.getLength())
        self.originalSeq = originalSeq
        self.normData = self.calculateNormalizedData() 
    
    '''override'''
    def getPoint(self, i):
        self.testIndex(i)
        return self.normData[i]
    
    '''override'''
    def getAllPoints(self):
        return self.normData
    
    '''Returns and normalizes'''
    def calculateNormalizedData(self):
        nMatrix = self.originalSeq.getAllPoints()
        mean = sum(nMatrix)/self.getLength()
        nMatrix = [(x-mean) for x in nMatrix]
        nMatrix = [(x/np.absolute(nMatrix).max()) for x in nMatrix]
        return nMatrix
    
    def getOriginal(self):
        return self.originalSeq
    
    '''Compares 2 sequences and return their Euclidean distance after being scaled to equal lengths'''
    def compare(self, other):
        if (self.getLength() == other.getLength()):
            return self.compareEuclDist(other)
        elif (self.getLength() < other.getLength()):
            scaledSeq = ScaledSequence(self, other.getLength())
            return scaledSeq.compareEuclDist(other)
        else:
            return other.compare(self)
    
    
class ScaledSequence(Sequence):
    
    def __init__(self, originalSeq, newLength):
        '''
        Constructor
        '''
        super().__init__(originalSeq.timeSeq, originalSeq.getStart(), originalSeq.getLength())
        self.originalSeq = originalSeq
        self.newLength = newLength
        self.scaledData = self.scaleToLength()
        
    def getLength(self):
        return self.newLength
        
    def getPoint(self, i):
        self.testIndex(i)
        return self.scaledData[i]
    
    def getAllPoints(self):
        return self.scaledData
    
    def getOriginal(self):
        return self.originalSeq
    
    '''Scales the data of this sequence to the length, newLength, and returns the scaledData'''
    def scaleToLength(self):
        scaledData = []
        for i in range(0, self.getLength()):
            j = math.floor(i * (self.getOriginal().getLength() / self.getLength()))
            scaledData.append(self.getOriginal().getPoint(j))
        return scaledData
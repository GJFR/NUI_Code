'''
Created on 26 nov. 2013

@author: Kevin
'''
import Sequence

class CompositeSequence(object):
    '''
    classdocs
    '''


    def __init__(self, seqA, seqB, valueA):
        '''
        Constructor
        '''
        self.seqA = seqA
        self.seqB = seqB
        self.valueA = valueA
        
        if seqA.getStart() != seqB.getStart() or seqA.getLength() != seqB.getLength():
            raise TypeError("De sequenties matchen niet")

    
    def compare(self, other):
        return self.valueA * self.seqA.compare(other.seqA) + (1 - self.valueA) * self.seqB.compare(other.seqB)
    
    def getStart(self):
        return self.seqA.getStart()
    
    def getLength(self):
        return self.seqA.getLength()
    
    def getDistance(self, other):
        return self.seqA.getDistance(other.seqA)
    
    def getWord(self, woordLengte, alfabetGrootte):
        return self.seqA.getWord(woordLengte, alfabetGrootte) + self.seqB.getWord(woordLengte, alfabetGrootte)
    
    
    
        '''override'''
    def __str__(self):
        return str(self.getStart()) + " (" + str(self.getLength()) + ")"
    
    '''override'''
    def __repr__(self):
        return str(self.getStart()) + " (" + str(self.getLength()) + ")"        
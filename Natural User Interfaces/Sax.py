'''
Created on 12 nov. 2013

@author: Kevin & Gertjan
'''
import scipy.stats

class TimeSequence(object):
    '''
    classdocs
    '''
    x = scipy.stats.norm(0,1)
    lst = " abcdefghijklmnopqrstuvwxyz"
    def __init__(self, data, sequentieLengte, woordLengte, alfabetGrootte):
        '''        Constructor        '''
        self.data = data
        self.sequentieLengte = sequentieLengte
        self.woordLengte = woordLengte
        self.alfabetGrootte = alfabetGrootte
    
    
    def getSaxArray(self):
        saxArray = []
        for i in range(len(self.data) - self.sequentieLengte):
            saxArray.append(self.getPAA(self.data[i:i+self.sequentieLengte]))
        return saxArray
     
    def getPAA(self, sequentie):
        word = ""
        for i in range(3):
            total = 0
            for j in range((self.sequentieLengte/self.woordLengte) * (i - 1) + 1,(self.sequentieLengte/self.woordLengte) * i + 1):
                total += sequentie[j]
            waarde = (self.woordLengte/self.sequentieLengte) * total
            word += self.getLetter(self.waarde, self.alfabetGrootte)
        return word
            
            
    def getLetter(self, waarde):
        letterWaarde = self.x.cdf(waarde) * self.alfabetGrootte
        for i in range(1,self.alfabetGrootte):
            if letterWaarde < i :
                return self.lst[i]
        
    def getCollisionMatrix(self):
        saxArray = self.getSaxArray()
        maskers = []
        cMatrix = [ [0 for y in range(self.sequentieLengte)] for x in range(self.sequentieLengte) ]
        for mask in maskers:
            buckets = fHash(saxArray,mask)
            checkBuckets(buckets, cMatrix)
        
        
    def fHash(self, saxArray, masker):
        
    def checkBuckets(self, buckets):
        
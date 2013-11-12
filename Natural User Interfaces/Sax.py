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
            buckets = self.fHash(saxArray,mask)
            self.checkBuckets(buckets, cMatrix)
            

    def mask(self, saxArray, masker):
        maskArray = []
        for word in saxArray:
            maskWord = ""
            for i in range(self.alfabetGrootte + 1):
                if not(i in masker):
                    maskWord += word[i]
            maskArray.append(maskWord)
        return maskArray
    
    def fHash(self, saxArray, masker):
        array = self.mask(saxArray, masker)
        buckets = {}
        for i in range(len(saxArray)):
            if (array[i] in buckets):
                buckets[array[i]].append(i)
            else:
                buckets[array[i]] = [i]
        return buckets
        
    
        
    def checkBuckets(self, buckets, cMatrix):
        for key in buckets:
            buckets[key].sort()
            for i in range(len(buckets[key])):
                for j in range(i+1,len(buckets[key])):
                    cMatrix[buckets[key][i]][buckets[key][j]] += 1

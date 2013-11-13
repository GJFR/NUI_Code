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
        print(saxArray)
        return saxArray
     
    def getPAA(self, sequentie):
        word = ""
        for i in range(self.woordLengte):
            total = 0
            for j in range(int((self.sequentieLengte/self.woordLengte) * (i - 1) + 1),int((self.sequentieLengte/self.woordLengte) * i) + 1):
                total += sequentie[j]
            waarde = (self.woordLengte/self.sequentieLengte) * total
            word += self.getLetter(waarde)
        return word
            
            
    def getLetter(self, waarde):
        letterWaarde = self.x.cdf(waarde) * self.alfabetGrootte
        for i in range(1,self.alfabetGrootte + 1):
            if letterWaarde < i :
                return self.lst[i]
        return ""
        
    def getCollisionMatrix(self):
        saxArray = self.getSaxArray()
        maskers = [[1,2],[2,3],[3,4],[1,3],[2,4],[1,4]]
        cMatrix = [ [0 for y in range(len(saxArray))] for x in range(len(saxArray)) ]
        for mask in maskers:
            buckets = self.fHash(saxArray,mask)
            self.checkBuckets(buckets, cMatrix)
        return cMatrix
    
    def mask(self, saxArray, masker):
        maskArray = []
        for word in saxArray:
            maskWord = ""
            for i in range(self.woordLengte):
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
            bucket = buckets[key]
            bucket.sort()
            for i in range(len(bucket)):
                for j in range(i+1,len(bucket)):
                    cMatrix[bucket[i]][bucket[j]] += 1

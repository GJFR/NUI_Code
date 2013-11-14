'''
Created on 12 nov. 2013

@author: Kevin & Gertjan
'''
import scipy.stats
import scipy.sparse
import itertools
import math

class TimeSequence(object):
    '''
    classdocs
    '''
    x = scipy.stats.norm(0,1)
    lst = " abcdefghijklmnopqrstuvwxyz"
    def __init__(self, data, sequentieLengte, woordLengte, alfabetGrootte, collisionThreshold, range):
        '''        Constructor        '''
        self.data = data
        self.sequentieLengte = sequentieLengte
        self.woordLengte = woordLengte
        self.alfabetGrootte = alfabetGrootte
        self.collisionThreshold = collisionThreshold
        self.range = range
    
    
    def getSaxArray(self):
        saxArray = []
        for i in range(len(self.data) - self.sequentieLengte):
            saxArray.append(self.getPAA(self.data[i:i+self.sequentieLengte]))
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
        maskers = [[1,2,3],[2,3,4],[3,4,5],[1,3,5],[0,2,4],[0,1,2]]
        '''cMatrix = [ [0 for y in range(len(saxArray))] for x in range(len(saxArray)) ]'''
        cMatrix = scipy.sparse.lil_matrix((len(saxArray),len(saxArray)))
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
                    cMatrix[bucket[i],bucket[j]] += 1
                    
    def iterateMatrix(self, cMatrix):
        cooMatrix = cMatrix.tocoo()
        thresholdList = []
        for i,j,v in itertools.zip_longest(cooMatrix.row, cooMatrix.col, cooMatrix.data):
            if v >= self.collisionThreshold:
                thresholdList.append((i,j))
        return thresholdList
    
    def calculateEuclDistance(self, sequence1, sequence2):
        som = 0
        for i in range(len(sequence1)):
            som += (sequence1[i] - sequence2[i])**2
        return math.sqrt(som)
    
    def calculateGoodMatches(self, cMatrix):
        pairs = self.iterateMatrix(cMatrix)
        dict = {}
        for (i,j) in pairs:
            eDist = self.calculateEuclDistance(self.data[i:i+self.sequentieLengte], self.data[j:j+self.sequentieLengte])
            if eDist <= self.range:
                if i in dict:
                    dict[i].append(j)
                else:
                    dict[i] = [j]
                if j in dict:
                    dict[j].append(i)
                else:
                    dict[j] = [i]
        
        order = []
        for i in dict:
            for j in range(len(order)-1,-1,-1):
                if len(dict[i]) < len(dict[order[j]]):
                    order.insert(j+1, i)
                    break
            else:
                order.insert(0,i)
            if len(order) > 5:
                order.pop(5)
        
        print ("a")
        self.removeCloseMatches(dict)
        print (str(order[0]) + ", " , dict[order[0]])
        return order
        
    def removeCloseMatches(self, dict):
        for key in dict:
            newList = []
            besteReeks = dict[key][0]
            besteDist = self.calculateEuclDistance(self.data[dict[key][0]:dict[key][0]+self.sequentieLengte], self.data[key:key+self.sequentieLengte])   
            for i in range(1,len(dict[key])):
                if dict[key][i] == dict[key][i-1] + 1:
                    newDist = self.calculateEuclDistance(self.data[dict[key][i]:dict[key][i]+self.sequentieLengte], self.data[key:key+self.sequentieLengte])
                    if(newDist < besteDist):
                        besteReeks = dict[key][i]
                        besteDist = newDist
                else:
                    newList.append(besteReeks)
                    besteReeks = dict[key][i]
                    besteDist = self.calculateEuclDistance(self.data[i:i+self.sequentieLengte], self.data[key:key+self.sequentieLengte])    
            else:
                newList.append(besteReeks)

            dict[key] = newList
            
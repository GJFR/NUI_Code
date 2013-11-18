'''
Created on 12 nov. 2013

@author: Kevin & Gertjan
'''
import scipy.stats
import scipy.sparse
import itertools
import Sequence
import time

class TimeSequence(object):
    '''
    classdocs
    '''
   
    def __init__(self, data, sequentieLengte, woordLengte, alfabetGrootte, collisionThreshold, r):
        '''        Constructor        '''
        self.data = data
        self.sequentieLengte = sequentieLengte
        self.woordLengte = woordLengte
        self.alfabetGrootte = alfabetGrootte
        self.collisionThreshold = collisionThreshold
        self.r = r
        self.sequenceList = []
        a = len(data) - self.sequentieLengte
        for index in range(a):
            normSeq = Sequence.Sequence(data, index, self.sequentieLengte).getNormalized()
            self.sequenceList.append(normSeq)
    
    
    def getSaxArray(self):
        saxArray = []
        for seq in self.sequenceList:
            saxArray.append(seq.getWord(self.woordLengte, self.alfabetGrootte))
        return saxArray
        
    def getCollisionMatrix(self):
        saxArray = self.getSaxArray()
        maskers = [[0,1,2,3,4],[1,2,3,4,5],[2,3,4,5,6],[3,4,5,6,7],[4,5,6,7,8],[5,6,7,8,9],[1,3,5,7,9],[0,2,4,6,8],[0,1,2,3,4],[5,6,7,8,9]]
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
        for seq in self.sequenceList:
            i = seq.start
            if (array[i] in buckets):
                buckets[array[i]].append(seq)
            else:
                buckets[array[i]] = [seq]
        return buckets
        
    
        
    def checkBuckets(self, buckets, cMatrix):
        for key in buckets:
            bucket = buckets[key]
            bucket.sort(key= lambda x : x.start)
            for i in range(len(bucket)):
                for j in range(i+1,len(bucket)):
                    cMatrix[bucket[i].start,bucket[j].start] += 1
                    
    def iterateMatrix(self, cMatrix):
        cooMatrix = cMatrix.tocoo()
        thresholdList = []
        for i,j,v in itertools.zip_longest(cooMatrix.row, cooMatrix.col, cooMatrix.data):
            if v >= self.collisionThreshold:
                thresholdList.append((self.sequenceList[i],self.sequenceList[j]))
        return thresholdList
    
    
    def calculateGoodMatches(self, cMatrix):
        tijd = time.time()
        pairs = self.iterateMatrix(cMatrix)
        self.checkpoint("iterateMatrix: ", tijd)
        
        
        diction = {}
        for (i,j) in pairs:
            eDist = i.compareEuclDist(j)
            if eDist <= self.r:
                if i in diction:
                    diction[i].append(j)
                else:
                    diction[i] = [j]
                if j in diction:
                    diction[j].append(i)
                else:
                    diction[j] = [i]
        
        tijd = time.time()
        self.removeCloseMatches(diction)
        pairs = self.iterateMatrix(cMatrix)
        self.checkpoint("removeCloseMatch: ", tijd)
        
        
        
        order = []
        for i in diction:
            '''for motif in order:
                if(abs(motif.start - i.start) < 25):
                    if len(diction[i]) > len(diction[motif]):
                        order.remove(motif)
                        order.append(i)
                    break'''
            for j in range(len(order)-1,-1,-1):
                if len(diction[i]) < len(diction[order[j]]):
                    order.insert(j+1, i)
                    break
            else:
                order.insert(0,i)
            if len(order) > 5:
                order.pop(5)
        
        '''returndiction = {}
        for motif in order:
            returndiction[motif] = diction[motif]'''
        dictionOrder = {}
        for motif in order:
            dictionOrder[motif.getOriginal()] = []
            for sequence in diction[motif]:
                dictionOrder[motif.getOriginal()].append(sequence.getOriginal())
        return dictionOrder
        
    def removeCloseMatches(self, diction):
        for motif in diction:
            newList = []
            motifList = diction[motif]
            besteReeks = motifList[0]
            besteDist = motif.compareEuclDist(besteReeks) 
            for i in range(1,len(motifList)):
                keyListItem = motifList[i]
                if keyListItem.start == motifList[i-1].start + 1:
                    newDist = motif.compareEuclDist(keyListItem)
                    if(newDist < besteDist):
                        besteReeks = keyListItem
                        besteDist = newDist
                else:
                    newList.append(besteReeks)
                    besteReeks = keyListItem
                    besteDist = motif.compareEuclDist(keyListItem)    
            else:
                newList.append(besteReeks)
            i = 0
            while i < len(newList):
                if (newList[i].start == motif.start - 1) or (newList[i].start == motif.start + 1):
                    newList.pop(i)
                else:
                    i += 1
            diction[motif] = newList
            
    def checkpoint(self, message, previousTime):
        tijd = time.time()
        print (message + str(tijd - previousTime))
        return tijd
'''
Created on 12 nov. 2013

@author: Kevin & Gertjan
'''
import scipy.stats
import scipy.sparse
import itertools
import Sequence
import time
import random

class TimeSequence(object):
    '''
    classdocs
    '''
   
    def __init__(self, data, minSeqLengte, maxSeqLengte, woordLengte, alfabetGrootte, collisionThreshold, r):
        '''        Constructor        '''
        self.data = data
        self.minSeqLengte = minSeqLengte
        self.maxSeqLengte = maxSeqLengte
        self.woordLengte = woordLengte
        self.alfabetGrootte = alfabetGrootte
        self.collisionThreshold = collisionThreshold
        self.r = r
        self.sequenceList = []
        for seqLengte in range(minSeqLengte,maxSeqLengte+1,10):
            a = len(data) - seqLengte
            for index in range(a):
                normSeq = Sequence.Sequence(data, index, seqLengte).getNormalized()
                self.sequenceList.append(normSeq)
    
    def getSaxArray(self):
        saxArray = []
        for seq in self.sequenceList:
            saxArray.append(seq.getWord(self.woordLengte, self.alfabetGrootte))
        return saxArray
        
    def getCollisionMatrix(self):
        saxArray = self.getSaxArray()
        '''maskers = [[0,1,2,3,4],[1,2,3,4,5],[2,3,4,5,6],[3,4,5,6,7],[4,5,6,7,8],[5,6,7,8,9],[1,3,5,7,9],[0,2,4,6,8],[0,1,2,3,4],[5,6,7,8,9]]'''
        maskers = self.makeMasks(self.woordLengte)
        print(maskers)
        cMatrix = scipy.sparse.lil_matrix((len(saxArray),len(saxArray)))
        for mask in maskers:
            buckets = self.fHash(saxArray,mask)
            self.checkBuckets(buckets, cMatrix)
        return cMatrix
    
    def makeMasks(self, aantal):
        masks = []
        while len(masks) < aantal:
            mask = []
            for j in range(0,self.woordLengte):
                if (random.random() > 0.5):
                    mask.append(j)
            for m in masks:
                if len(m) != len(mask):
                    continue
                for element in m:
                    if not(element in mask):
                        break
                else:
                    break
            else:
                masks.append(mask)
        return masks
    
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
        for i in range(len(self.sequenceList)):
            if (array[i] in buckets):
                buckets[array[i]].append(self.sequenceList[i])
            else:
                buckets[array[i]] = [self.sequenceList[i]]
        return buckets
        
    def checkBuckets(self, buckets, cMatrix):
        for key in buckets:
            bucket = buckets[key]
            bucket.sort(key= lambda x : x.getStart())
            for i in range(len(bucket)):
                for j in range(i+1,len(bucket)):
                    cMatrix[bucket[i].getStart(),bucket[j].getStart()] += 1
                    
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
        tijd = self.checkpoint("iterateMatrix: ", tijd)
        
        diction = {}
        for (motif,index) in pairs:
            eDist = motif.compare(index)
            if eDist <= self.r:
                if motif in diction:
                    diction[motif].append(index)
                else:
                    diction[motif] = [index]
                if index in diction:
                    diction[index].append(motif)
                else:
                    diction[index] = [motif]
        
        tijd = self.checkpoint("makeDictionary: ", tijd)
        self.removeCloseMatches(diction)
        pairs = self.iterateMatrix(cMatrix)
        self.checkpoint("removeCloseMatch: ", tijd)
        
        
        
        order = []
        for motif in diction:
            for index in range(len(order)-1,-1,-1):
                if abs(motif.getStart() - order[index].getStart()) <= 100 :
                    if len(diction[motif]) > len(diction[order[index]]):
                        order.pop(index)
                    else:
                        break
            else:
                for index in range(len(order)-1,-1,-1):
                    if len(diction[motif]) < len(diction[order[index]]):
                        order.insert(index+1, motif)
                        break
                else:
                    order.insert(0,motif)
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
            besteDist = motif.compare(besteReeks) 
            for i in range(1,len(motifList)):
                keyListItem = motifList[i]
                if keyListItem.getStart() == motifList[i-1].getStart() + 1:
                    newDist = motif.compare(keyListItem)
                    if(newDist < besteDist):
                        besteReeks = keyListItem
                        besteDist = newDist
                else:
                    newList.append(besteReeks)
                    besteReeks = keyListItem
                    besteDist = motif.compare(keyListItem)    
            else:
                newList.append(besteReeks)
            i = len(newList) - 1
            while i >= 0:
                if abs(newList[i].getStart() - motif.getStart()) <= 100 :
                    newList.pop(i)
                i -= 1
            diction[motif] = newList
            
    def checkpoint(self, message, previousTime):
        tijd = time.time()
        print (message + str(tijd - previousTime))
        return tijd
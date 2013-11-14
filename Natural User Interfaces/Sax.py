'''
Created on 12 nov. 2013

@author: Kevin & Gertjan
'''
import scipy.stats
import scipy.sparse
import itertools
import Sequence

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
        maskers = [[1,2,3],[2,3,4],[3,4,5],[1,3,5],[0,2,4],[0,1,2]]
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
        pairs = self.iterateMatrix(cMatrix)
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
        
        order = []
        for i in diction:
            for j in range(len(order)-1,-1,-1):
                if len(diction[i]) < len(diction[order[j]]):
                    order.insert(j+1, i)
                    break
            else:
                order.insert(0,i)
            if len(order) > 5:
                order.pop(5)
        
        self.removeCloseMatches(diction)
        print (str(order[0]) + ", " , diction[order[0]])
        '''returndiction = {}
        for motif in order:
            returndiction[motif] = diction[motif]'''
        return diction[order[0]]
        
    def removeCloseMatches(self, diction):
        for key in diction:
            newList = []
            keyList = diction[key]
            besteReeks = keyList[0]
            besteDist = key.compareEuclDist(besteReeks) 
            for i in range(1,len(keyList)):
                keyListItem = keyList[i]
                if keyListItem.start == keyList[i-1].start + 1:
                    newDist = key.compareEuclDist(keyListItem)
                    if(newDist < besteDist):
                        besteReeks = keyListItem
                        besteDist = newDist
                else:
                    newList.append(besteReeks)
                    besteReeks = keyListItem
                    besteDist = key.compareEuclDist(keyListItem)    
            else:
                newList.append(besteReeks)

            diction[key] = newList
            
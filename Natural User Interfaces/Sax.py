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
    
#     def makeMasks(self, aantal):
#         masks = []
#         while len(masks) < aantal:
#             mask = []
#             for j in range(0,self.woordLengte):
#                 if (random.random() > 0.5):
#                     mask.append(j)
#             for m in masks:
#                 if len(m) != len(mask):
#                     continue
#                 for element in m:
#                     if not(element in mask):
#                         break
#                 else:
#                     break
#             else:
#                 masks.append(mask)
#         return masks

    def makeMasks(self, aantal):
        masks = []
        while len(masks) < aantal:
            maskLengte = random.randrange(1,self.woordLengte/2)
            mask = []
            while len(mask) < maskLengte:
                punt = random.randrange(self.woordLengte)
                if not(punt in mask):
                    mask.append(punt)
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

    """ gesStart werd op geroepen om te weten te komen welke rij en kolom men moest verhogen bij checkBuckets
    bij uniforme schaling werkt dit natuurlijk niet meer.
    
    ipv sequences in buckets te steken doen we nu de positie in de sequenceList,
    anders moesten we de hele sequenceList overlopen om te weten te komen welk nummer bij welke sequentie hoort.
    cMatrix heeft immers een nummer nodig, want daar zijn de indexen integers"""
    def fHash(self, saxArray, masker):
        array = self.mask(saxArray, masker)
        buckets = {}
        for i in range(len(self.sequenceList)):
            if (array[i] in buckets):
                buckets[array[i]].append(i)
            else:
                buckets[array[i]] = [i]
        return buckets
    
    def checkBuckets(self, buckets, cMatrix):
        for key in buckets:
            bucket = buckets[key]
            for i in range(len(bucket)):
                for j in range(i+1,len(bucket)):
                    cMatrix[bucket[i],bucket[j]] += 1
               
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
        
#     def removeCloseMatches(self, diction):
#         for motif in diction:
#             newList = []
#             motifList = diction[motif]
#             motifList.sort(key = lambda x: x.getStart())
#             besteReeks = motifList[0]
#             besteDist = motif.compare(besteReeks) 
#             for i in range(1,len(motifList)):
#                 keyListItem = motifList[i]
#                 if keyListItem.getStart() == motifList[i-1].getStart() + 1 or keyListItem.getStart() == motifList[i-1].getStart() :
#                     newDist = motif.compare(keyListItem)
#                     if(newDist < besteDist):
#                         besteReeks = keyListItem
#                         besteDist = newDist
#                 else:
#                     newList.append(besteReeks)
#                     besteReeks = keyListItem
#                     besteDist = motif.compare(keyListItem)    
#             else:
#                 newList.append(besteReeks)
#             i = len(newList) - 1
#             while i >= 0:
#                 if abs(newList[i].getStart() - motif.getStart()) <= 100 :
#                     newList.pop(i)
#                 i -= 1
#             diction[motif] = newList

    def removeCloseMatches(self, diction):
        for motif in diction:
            volledigeLijst = [x for x in diction[motif]]
            volledigeLijst.append(motif)
            removeList = []
            for seq1 in volledigeLijst:
                for seq2 in volledigeLijst:
                    if seq1 == seq2:
                        continue
                    eerste =  min(seq1, seq2, key = lambda x: x.getStart())
                    if abs(seq1.getStart() - seq2.getStart()) < eerste.getLength():
                        if motif.compare(seq1) < motif.compare(seq2):
                            removeList.append(seq2)
                        else:
                            removeList.append(seq1)
                            
            volledigeLijst = [x for x in volledigeLijst if x not in removeList]
            
            removeList.sort(key = lambda x: motif.compare(x))
            for rem in removeList:
                for seq in volledigeLijst:
                    eerste =  min(rem, seq, key = lambda x: x.getStart())
                    if abs(rem.getStart() - seq.getStart()) < eerste.getLength():
                        break
                else:
                    volledigeLijst.append(rem)
            volledigeLijst.remove(motif)
            diction[motif] = volledigeLijst
                   
    def checkpoint(self, message, previousTime):
        tijd = time.time()
        print (message + str(tijd - previousTime))
        return tijd
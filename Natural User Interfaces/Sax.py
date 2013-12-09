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
import math

class TimeSequence(object):
    '''
    classdocs
    '''
    MIN_AFSTAND = 75
    def __init__(self, data, verdeelPunten, minSeqLengte, maxSeqLengte, woordLengte, alfabetGrootte, collisionThreshold, r):
        '''        Constructor        '''
        self.data = data
        self.verdeelPunten = verdeelPunten
        if verdeelPunten[-1] > len(data):
            raise AttributeError("verdeelpunten groter dan de lengte")
        self.minSeqLengte = minSeqLengte
        self.maxSeqLengte = maxSeqLengte
        if woordLengte > minSeqLengte:
            raise AttributeError("woordLengte groter dan minSeqLengte")
        self.woordLengte = woordLengte
        self.alfabetGrootte = alfabetGrootte
        self.collisionThreshold = collisionThreshold
        self.r = r
        self.sequenceList = []
        self.sequenceHash = {}
        self.groupHash = {}
        for i in range(len(verdeelPunten)-1):
            begin = verdeelPunten[i]
            einde = verdeelPunten[i+1]
            self.groupHash[i] = []
            for seqLengte in range(minSeqLengte,maxSeqLengte+1,math.ceil(maxSeqLengte*0.03)):
                a = einde - seqLengte
                for j in range(begin,a+1):
                    normSeq = Sequence.Sequence(data, j, seqLengte).getNormalized()
                    self.sequenceList.append(normSeq)
                    self.sequenceHash[normSeq] = i
                    self.groupHash[i].append(normSeq)
    
    '''Returns the SAX-array of this timesequence.'''
    def getSaxArray(self):
        saxArray = []
        for seq in self.sequenceList:
            saxArray.append(seq.getWord(self.woordLengte, self.alfabetGrootte))
        return saxArray
    
    '''Returns the collission matrix of this timesequence, using makeMaks() to generate the needed masks.'''
    def getCollisionMatrix(self, masks):
        saxArray = self.getSaxArray()
        
        cMatrix = scipy.sparse.lil_matrix((len(saxArray),len(saxArray)))
        for mask in masks:
            buckets = self.fHash(saxArray,mask)
            self.checkBuckets(buckets, cMatrix)
        return cMatrix

    '''Returns a random generated list of masks (who satisfy our conditions)'''
    def getMasks(self):
        masks = []
        while len(masks) < self.woordLengte:
            maskLengte = random.randrange(1,self.woordLengte)
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
    
    '''Returns a masked version of the given SAX-array by the given masks'''
    def mask(self, saxArray, mask):
        maskedSaxArray = []
        for word in saxArray:
            maskWord = ""
            for i in range(self.woordLengte):
                if not(i in mask):
                    maskWord += word[i]
            maskedSaxArray.append(maskWord)
        return maskedSaxArray

    '''Returns a list of buckets to which the given SAX-array entries hash, using the given masks.'''
    def fHash(self, saxArray, masker):
        array = self.mask(saxArray, masker)
        buckets = {}
        for i in range(len(self.sequenceList)):
            if (array[i] in buckets):
                buckets[array[i]].append(i)
            else:
                buckets[array[i]] = [i]
        return buckets
    
    '''Iterates through the given buckets and increments each cell of the given collision matrix when there is a hashing collision'''
    def checkBuckets(self, buckets, cMatrix):
        for key in buckets:
            bucket = buckets[key]
            for i in range(len(bucket)):
                for j in range(i+1,len(bucket)):
                    if self.test(bucket[i],bucket[j]):
                        cMatrix[bucket[i],bucket[j]] += 1

    def test(self, i, j):
        return self.sequenceHash[self.sequenceList[i]] == self.sequenceHash[self.sequenceList[j]]

    '''Returns a list of all pairs of sequences who's number of collisions is higher than the collision threshold.'''
    def getLikelyPairs(self, cMatrix):
        cooMatrix = cMatrix.tocoo()
        thresholdList = []
        for i,j,v in itertools.zip_longest(cooMatrix.row, cooMatrix.col, cooMatrix.data):
            if v >= self.collisionThreshold:
                thresholdList.append((self.sequenceList[i],self.sequenceList[j]))
        return thresholdList
    
    def getMotifs(self, cMatrix):
        pairs = self.getLikelyPairs(cMatrix)
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
        return diction
    
    def getTopXMotifs(self, topX, diction):
        diction2 = sorted(diction.keys(), key = lambda x: len(diction[x]), reverse = True)
        it = iter(diction2)
        topX = {}
        while (len(topX) < 5):
            try:
                motif = next(it)
            except:
                break
            topX[motif] = diction[motif]
            temp = {motif: topX[motif]}
            self.removeCloseMatches(temp)
            topX[motif] = temp[motif]
            self.removeTrivialMotifs(topX)
        return topX

    def removeCloseMatches(self, matchDistDict):
        for motif in matchDistDict:
            groupMatch = {}
            for match,dist in matchDistDict[motif]:
                group = self.sequenceHash[match]
                if group in groupMatch:
                    bSeq,bDist = groupMatch[group]
                    if dist < bDist:
                        groupMatch[group] = (match,dist)
                else:
                    groupMatch[group] = (match,dist)
            matchDistDict[motif] = []
            for match,dist in groupMatch.values():
                matchDistDict[motif].append((match,dist))
            
    def makeMatchDistancePair(self,diction):
        newD = {}
        for motif in diction:
            newD[motif] = []
            for seq in diction[motif]:
                dist = motif.compare(seq)
                newD[motif].append((seq,dist))
        return newD
    
    
    def removeTrivialMotifs(self, diction):
        #verwijder dichtbij elkaarliggende motieven
        motifList = []
        for motif in diction:
            motifList.append(motif)
        
        removeList = []
        for i in range(len(motifList)):
            mot1 = motifList[i]
            for j in range(i+1, len(motifList)):
                mot2 = motifList[j]
                eerste =  min(mot1, mot2, key = lambda x: x.getStart())
                if mot1.getDistance(mot2) < eerste.getLength():
                    if len(diction[mot1]) == len(diction[mot2]):
                        if mot1.getLength() < mot2.getLength():
                            removeList.append(mot2)
                        else:
                            removeList.append(mot1)
                    else:
                        slechtste = min(mot1, mot2, key = lambda x: len(diction[x]))
                        removeList.append(slechtste)
            
        motifList = [x for x in motifList if x not in removeList]
         
        removeList.sort(key = lambda x: (len(diction[x]), x.getLength()))
        for rem in removeList:
            for mot in motifList:
                eerste =  min(rem, mot, key = lambda x: x.getStart())
                if rem.getDistance(mot) < eerste.getLength():
                    break
            else:
                motifList.append(rem)
        
        
        # verwijder dezelfde motifs (in elkaars groep)
        removeList = []
        motInSeq = {}
        for mot in motifList:
            motInSeq[mot] = [x for x in diction[mot]]
            motInSeq[mot].append(mot)
                 
        for mot1 in motifList:
            motList1 = motInSeq[mot1]
            if len(motList1) == 1:
                removeList.append(mot1)
                continue
            for mot2 in motifList:
                motList2 = motInSeq[mot2]
                if mot1 == mot2 or len(motList2) == 1 or mot2 in removeList:
                    continue
                if self.isSequenceSubsetOf(mot1,mot2,motList1,motList2):
                    removeList.append(mot1)
        
        for mot in removeList:
            if mot in motifList:
                motifList.remove(mot)
        
        '''filter hier motifList uit diction'''
        removeList = [x for x in diction if x not in motifList]
        for mot in removeList:
            del diction[mot]
            
    def getBestMotifs(self, diction):
        it = iter(diction)
        aantalGroepen = len(self.verdeelPunten) - 1
        bestMotif = None
        bestDist = self.r * aantalGroepen
        while it.has:
            motif = it.next()
            dist = self.getTotalDistance(motif, diction[motif])
            if dist < bestDist and diction[motif] >= aantalGroepen:
                bestMotif = motif
                bestDist = dist
        if (bestMotif == None):
            raise Exception("No best motif was found.")
        return bestMotif
    
    def getTotalDistance(self, matchDistPairs):
        dist = 0
        for match,dist in matchDistPairs:
            dist += dist
        return dist
        
    def isSequenceSubsetOf(self, mot1, mot2, motList1, motList2):
        
        for elem1 in motList1:
            for elem2 in motList2:
                if elem1.getDistance(elem2) <= self.MIN_AFSTAND:
                    break
            else:
                return False
        if len(motList1) == len(motList2):
            total1 = 0
            for seq in motList1:
                total1 += mot1.compare(seq)
            total2 = 0
            for seq in motList2:
                total2 += mot2.compare(seq)
            if(total1 < total2):
                return False
        return True

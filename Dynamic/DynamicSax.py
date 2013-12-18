'''
Created on 9-dec.-2013

@author: Kevin & Gertjan
'''
import scipy.stats
import scipy.sparse
import itertools
import Sequence
import time
import random
import math

class DynamicTimeSeq(object):
    '''
    classdocs
    '''
    MIN_AFSTAND = 75
    def __init__(self, minSeqLengte, maxSeqLengte, woordLengte, alfabetGrootte, collisionThreshold, r):
        '''        Constructor        '''
        self.minSeqLengte = minSeqLengte
        self.maxSeqLengte = maxSeqLengte
        if woordLengte > minSeqLengte:
            raise AttributeError("woordLengte groter dan minSeqLengte")
        self.woordLengte = woordLengte
        self.alfabetGrootte = alfabetGrootte
        self.collisionThreshold = collisionThreshold
        self.r = r
        self.motifs = {}
        self.numberOfGroups = 0
        self.pairs = []
        self.masks = self.getMasks()
        self.sequenceHash = {}
        self.maskDict = {}
        self.maskKeys = {}
        for mask in self.masks:
            key = self.calculateKey(mask)
            self.maskKeys[key] = mask
            self.maskDict[key] = []
        self.sequenceList = []
    
    def addSequenceGroup(self, pair):
        group, sequenceHash = pair
        if self.numberOfGroups == 0:
            self.numberOfGroups += 1
            self.sequenceList = self.sequenceList + group
            self.sequenceHash.update(sequenceHash)
            return
        
        cMatrix = self.getCollisionMatrix(self.masks, sequenceHash)
        self.pairs = self.pairs + self.makeMatchDistancePair(cMatrix, group)
        self.numberOfGroups += 1
        self.sequenceList = self.sequenceList + group
        self.sequenceHash.update(sequenceHash)
        
    def getNumberOfGroups(self):
        return self.numberOfGroups
    
    '''Returns the SAX-array of this timesequence.'''
    def getSaxArray(self, group):
        saxArray = []
        for seq in group:
            saxArray.append(seq.getWord(self.woordLengte, self.alfabetGrootte))
        return saxArray
    
    '''Returns the collission matrix of this timesequence, using makeMaks() to generate the needed masks.'''
    def getCollisionMatrix(self, masks, group):
        saxArray = self.getSaxArray(group)
        
        cMatrix = scipy.sparse.lil_matrix((len(saxArray),len(self.sequenceList)))
        for maskKey in self.maskKeys:
            mask = self.maskKeys[maskKey]
            array = self.mask(saxArray, mask)
            buckets = self.fHash(array)
            self.checkBuckets(buckets, maskKey, cMatrix)
            self.maskDict[maskKey] = self.maskDict[maskKey] + array
        return cMatrix

    '''Returns a random generated list of masks (who satisfy our conditions)'''
    def getMasks(self):
        masks = []
        maskLengte = self.woordLengte * 1 / 4
        while len(masks) < self.woordLengte:
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
    
    def calculateKey(self, mask):
        key = ""
        for number in mask:
            key = key + str(number) + "-"
        return key
    
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
    def fHash(self, saxArray):
        buckets = {}
        for i in range(len(saxArray)):
            if (saxArray[i] in buckets):
                buckets[saxArray[i]].append(i)
            else:
                buckets[saxArray[i]] = [i]
        
        return buckets
    
    '''Iterates through the given buckets and increments each cell of the given collision matrix when there is a hashing collision'''
    def checkBuckets(self, buckets, maskKey, cMatrix):
        for index in range(len(self.maskDict[maskKey])):
            for seq in buckets.get(self.maskDict[maskKey][index], []):
                cMatrix[seq,index] += 1
            

    def test(self, i, j):
        return self.sequenceHash[self.sequenceList[i]] != self.sequenceHash[self.sequenceList[j]]

    '''Returns a list of all pairs of sequences who's number of collisions is higher than the collision threshold.'''
    def getLikelyPairs(self, cMatrix, group):
        cooMatrix = cMatrix.tocoo()
        thresholdList = []
        for i,j,v in itertools.zip_longest(cooMatrix.row, cooMatrix.col, cooMatrix.data):
            if v >= self.collisionThreshold:
                thresholdList.append((group[i],self.sequenceList[j]))
        return thresholdList
    
    def getMotifs(self):
        return self.motifs
    
    def calculateMotifs(self):
        diction = {}
        for (seq1,seq2,dist) in self.pairs:
            if dist <= self.r:
                if seq1 in diction:
                    diction[seq1].append((seq2,dist))
                else:
                    diction[seq1] = [(seq2,dist)]
                if seq2 in diction:
                    diction[seq2].append((seq1,dist))
                else:
                    diction[seq2] = [(seq1,dist)]
        self.motifs = diction
    
    def getTopXMotifs(self, topX):
        diction2 = sorted(self.motifs.keys(), key = lambda x: len(self.motifs[x]), reverse = True)
        it = iter(diction2)
        topX = {}
        while (len(topX) < 5):
            try:
                motif = next(it)
            except:
                break
            topX[motif] = self.motifs[motif]
            temp = {motif: topX[motif]}
            self.removeCloseMatches(temp)
            topX[motif] = temp[motif]
            self.removeTrivialMotifs(topX)
        return topX

    def removeCloseMatches(self):
        for motif in self.motifs:
            groupMatch = {}
            for match,dist in self.motifs[motif]:
                group = self.sequenceHash[match]
                if group in groupMatch:
                    bSeq,bDist = groupMatch[group]
                    if dist < bDist:
                        groupMatch[group] = (match,dist)
                else:
                    groupMatch[group] = (match,dist)
            self.motifs[motif] = []
            for match,dist in groupMatch.values():
                self.motifs[motif].append((match,dist))
            
    def makeMatchDistancePair(self,cMatrix, group):
        pairs = self.getLikelyPairs(cMatrix, group)
        newL = []
        for seq1,seq2 in pairs:
            dist = seq1.compare(seq2)
            newL.append((seq1,seq2,dist))
        return newL
    
    
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
            
    def getBestMotifs(self, nbMotifs):
        motifs = sorted(self.motifs.keys(),key=lambda motif: self.getTotalDistance(self.motifs[motif]))
        it = iter(sorted(motifs, key=lambda motif: len(self.motifs[motif]), reverse=True))
        bestMotifs = []
        while len(bestMotifs) < nbMotifs:
            try:
                motif = next(it)
            except StopIteration:
                break
            for m in bestMotifs:
                if motif.compare(m) < self.r:
                    break
            else:
                bestMotifs.append(motif)
                    
        if (len(bestMotifs) < nbMotifs):
            raise Exception("Not enough best motifs found.")
        return bestMotifs
    
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

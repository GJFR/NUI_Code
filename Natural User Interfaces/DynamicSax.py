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
    def __init__(self, wordLength, alphabetSize, collisionThreshold, r, heightDifference):
        '''        Constructor        '''
        self.woordLengte = wordLength
        self.alfabetGrootte = alphabetSize
        self.collisionThreshold = collisionThreshold
        self.r = r
        self.heightDifference = heightDifference
        '''motifs: Sequence -> Lijst van matches (sequenties) '''
        self.motifs = {}
        self.numberOfGroups = 0
        self.pairs = []
        self.masks = self.getMasks()
        print("masks : " + str(self.masks))
        '''sequenceHash: Sequence -> Groepnummer '''
        self.sequenceHash = {}
        '''maskDict: mask-key -> met dat masker gemaskerde sax-woorden'''
        self.maskDict = {}
        '''maskKeys: mask-key -> masker met die key'''
        self.maskKeys = {}
        for mask in self.masks:
            key = self.calculateKey(mask)
            self.maskKeys[key] = mask
            self.maskDict[key] = []
        self.sequenceList = []
    
    def addSequenceGroup(self, pair):
        newSequences, newSequenceHash = pair
        
        if self.numberOfGroups == 0:
            self.numberOfGroups += 1
            self.sequenceList = self.sequenceList + newSequences
            self.sequenceHash.update(newSequenceHash)
            self.fillMaskDict(self.masks, newSequences)
            return
            
        cMatrix = self.getCollisionMatrix(self.masks, newSequences)
        self.pairs = self.pairs + self.makeMatchDistancePair(cMatrix, newSequences)
        self.pairs = sorted(self.pairs, key=lambda a:self.takeDist(a))
        print(str(self.pairs[:10]))
        self.numberOfGroups += 1
        self.sequenceList = self.sequenceList + newSequences
        self.sequenceHash.update(newSequenceHash)
    
    def takeDist(self,a):
        seq1,seq2,dist = a
        return dist
    
    def getNumberOfGroups(self):
        return self.numberOfGroups
    
    '''Returns the SAX-array of this timesequence.'''
    def getSaxArray(self, group):
        saxArray = []
        for seq in group:
            saxArray.append(seq.getWord(self.woordLengte, self.alfabetGrootte))
        return saxArray
    
    def fillMaskDict(self,masks,group):
        saxArray = self.getSaxArray(group)
        
        for maskKey in self.maskKeys:
            mask = self.maskKeys[maskKey]
            array = self.mask(saxArray, mask)
            self.maskDict[maskKey] = self.maskDict[maskKey] + array
    
    '''Returns the collission matrix of this timesequence'''
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
        random.seed(0)
        masks = []
        maskLengte = self.woordLengte * 1 / 2
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
    
    def orderMotifs(self, motifs):
        matches = {}
        for motif in motifs:
            matches[motif] = motif
            for match,afstand in self.getMotifs()[motif]:
                if self.sequenceHash[match] < self.sequenceHash[matches[motif]]:
                    matches[motif] = match
        return sorted(motifs, key=lambda motif: matches[motif].getStart())
    
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
            if v >= self.collisionThreshold and group[i].getRealHeight() >= self.heightDifference and self.sequenceList[j].getRealHeight() >= self.heightDifference:
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
                if self.overlappen(motif,m):
                    break
            else:
                bestMotifs.append(motif)
                    
        if (len(bestMotifs) < nbMotifs):
            raise Exception("Not enough best motifs found.")
        return bestMotifs
    
    def overlappen(self, motif1, motif2):
        if self.sequenceHash[motif1] == self.sequenceHash[motif2] and motif1.overlap(motif2):
            return True
        for match2,comp in self.motifs[motif2]:
            if self.sequenceHash[motif1] == self.sequenceHash[match2] and motif1.overlap(match2):
                return True
        for match1,comp in self.motifs[motif1]:
            if self.sequenceHash[match1] == self.sequenceHash[motif2] and motif2.overlap(match1):
                return True
        for match1,comp in self.motifs[motif1]:
            for match2,comp in self.motifs[motif2]:
                if self.sequenceHash[match1] == self.sequenceHash[match2] and match1.overlap(match2):
                    return True
        return False
    
    def getTotalDistance(self, matchDistPairs):
        dist = 0
        for match,dist in matchDistPairs:
            dist += dist
        return dist

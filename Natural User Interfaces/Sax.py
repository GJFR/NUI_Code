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
import CompositeSequence

class TimeSequence(object):
    '''
    classdocs
    '''
    MIN_AFSTAND = 75
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
    
    '''Returns the SAX-array of this timesequence.'''
    def getSaxArray(self):
        saxArray = []
        for seq in self.sequenceList:
            saxArray.append(seq.getWord(self.woordLengte, self.alfabetGrootte))
        return saxArray
    
    '''Returns the collssion matrix of this timesequence, using makeMaks() to generate the needed masks.'''
    def getCollisionMatrix(self, masks):
        saxArray = self.getSaxArray()
        '''maskers = [[0,1,2,3,4],[1,2,3,4,5],[2,3,4,5,6],[3,4,5,6,7],[4,5,6,7,8],[5,6,7,8,9],[1,3,5,7,9],[0,2,4,6,8],[0,1,2,3,4],[5,6,7,8,9]]'''
        print(masks)
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
                    cMatrix[bucket[i],bucket[j]] += 1
    
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
    
    ''''''
    #===========================================================================
    # def calculateGoodMatches(self, cMatrix):
    #     tijd = time.time()
    #     pairs = self.getLikelyPairs(cMatrix)
    #     tijd = self.checkpoint("getLikelyPairs: ", tijd)
    #     
    #     diction = self.getMotifs()
    #     
    #     tijd = self.checkpoint("makeDictionary: ", tijd)
    #     
    #     diction = self.getTopXMotifs(5, diction)
    #         
    #     self.checkpoint("removeCloseMatch: ", tijd)
    #     
    #     '''
    #     Elke keer dat er in deze loop 'motif' werd gebruikt, werd motif.getOriginal() opgeroepen, maar die bestaat natuurlijk niet.
    #     Toen ik dit weg had gedaan, liep alles goed. Enkel toonde nu de grafiek de motieven als genormaliseerde sequenties, dus heb ik
    #     in Visualize.py pas gezorgd dat de afzonderlijke sequenties hun originele sequenties oproepen.
    #     '''
    #     return diction
    #===========================================================================

    def removeCloseMatches(self, diction):
        for motif in diction:
            volledigeLijst = [x for x in diction[motif]]
            volledigeLijst.append(motif)
            removeList = []
            for i in range(len(volledigeLijst)):
                seq1 = volledigeLijst[i]
                for j in range(i+1,len(volledigeLijst)):
                    seq2 = volledigeLijst[j]
                    eerste =  min(seq1, seq2, key = lambda x: x.getStart())
                    if seq1.getDistance(seq2) < eerste.getLength():
                        if motif.compare(seq1) < motif.compare(seq2):
                            removeList.append(seq2)
                        else:
                            removeList.append(seq1)
                             
            volledigeLijst = [x for x in volledigeLijst if x not in removeList]
             
            removeList.sort(key = lambda x: motif.compare(x))
            for rem in removeList:
                for seq in volledigeLijst:
                    eerste =  min(rem, seq, key = lambda x: x.getStart())
                    if rem.getDistance(seq) < eerste.getLength():
                        break
                else:
                    volledigeLijst.append(rem)
            volledigeLijst.remove(motif)
            diction[motif] = volledigeLijst
    
    
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
            if len(motInSeq[mot1]) == 1:
                removeList.append(mot1)
                continue
            for mot2 in motifList:
                if mot1 == mot2 or len(motInSeq[mot2]) == 1:
                    continue
                if self.isSequenceSubsetOf(mot1,mot2,motInSeq):
                    removeList.append(mot1)
        
        for mot in removeList:
            if mot in motifList:
                motifList.remove(mot)
        
        '''filter hier motifList uit diction'''
        removeList = [x for x in diction if x not in motifList]
        for mot in removeList:
            del diction[mot]
        
    def isSequenceSubsetOf(self, mot1, mot2, motInSeq):
        
        for elem1 in motInSeq[mot1]:
            for elem2 in motInSeq[mot2]:
                if elem1.getDistance(elem2) <= self.MIN_AFSTAND:
                    break
            else:
                return False
        if len(motInSeq[mot1]) == len(motInSeq[mot2]):
            total1 = 0
            for seq in motInSeq[mot1]:
                total1 += mot1.compare(seq)
            total2 = 0
            for seq in motInSeq[mot2]:
                total2 += mot2.compare(seq)
            if(total1 < total2):
                return False
        return True
    
    '''Prints the elapsed time and returns the current time'''
    def checkpoint(self, message, previousTime):
        tijd = time.time()
        print (message + str(tijd - previousTime))
        return tijd
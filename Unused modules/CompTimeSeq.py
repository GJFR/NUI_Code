'''
Created on 27-nov.-2013

@author: Gertjan
'''
import itertools
import CompositeSequence

class CompTimeSeq(object):
    '''
    classdocs
    '''


    def __init__(self, ts1, ts2, cMatrix, valueA):
        '''
        Constructor
        '''
        self.ts1 = ts1
        self.ts2 = ts2
        self.cMatrix = cMatrix
        compSeqList = []
        
        
    '''Returns a list of all pairs of sequences who's number of collisions is higher than the collision threshold.'''
    def getLikelyPairs(self, cMatrix):
        cooMatrix = cMatrix.tocoo()
        thresholdList = []
        for i,j,v in itertools.zip_longest(cooMatrix.row, cooMatrix.col, cooMatrix.data):
            if v >= self.collisionThreshold:
                thresholdList.append((CompositeSequence(self.ts1.sequenceList[i], self.ts2.sequenceList[i], self.valueA), CompositeSequence(self.ts1.sequenceList[j], self.ts2.sequenceList[j], self.valueA)))
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
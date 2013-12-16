'''
Created on 16-dec.-2013

@author: Kevin & Gertjan
'''
import random

class SeqChecker(object):
    '''
    classdocs
    '''


    def __init__(self, labeling, woordLengte, alfabetGrootte, collisionThreshold, r):
        '''
        Constructor
        '''
        self.labeling = labeling
        self.states = {}
        for label in labeling:
            self.states[label] = 0
        self.woordLengte = woordLengte
        self.alfabetGrootte = alfabetGrootte
        self.collisionThreshold = collisionThreshold
        self.r = r
        self.masks = self.getMasks()
        self.maskedLabeling = {}
        for label in labeling:
            self.maskedLabeling[label] = []
            saxArray = self.getSaxArray(self.labeling[label])
            for masker in self.masks:
                self.maskedLabeling[label].append(self.mask(saxArray,masker))
                
    def checkSequence(self, sequence):
        possibleLabels = self.saxCheck(sequence)
        matchLabels = self.rangeCheck(possibleLabels, sequence)
        for label in matchLabels:
            if self.incrementState(label):
                self.resetStates()
                return label
        return None
            
    def incrementState(self, label):
        self.states[label] += 1
        if self.states[label] >= len(self.labeling[label]):
            return True
        else:
            return False
    
    def resetStates(self):
        for label in self.labeling:
            self.states[label] = 0
        
    def saxCheck(self, sequence):
        word = [sequence.getWord(self.woordLengte, self.alfabetGrootte)]
        counters = {}
        for label in self.labeling:
            counters[label] = 0
        for i in range(len(self.masks)):
            maskedWord = self.mask(word, self.masks[i])
            for label in self.labeling:
                if maskedWord == self.maskedLabeling[label][i]:
                    counters[label] += 1
        
        possibleLabels = []
        for label in self.labeling:    
            if self.collisionThreshold <= counters[label]:
                possibleLabels.append(label)
        return possibleLabels
    
    def rangeCheck(self, possibleLabels, sequence):
        matchLabels = []
        for label in possibleLabels:
            if self.r >= self.labeling[label][self.states[label]].compare(sequence):
                matchLabels.append(label)
        return matchLabels
    
    '''Returns the SAX-array of this timesequence.'''
    def getSaxArray(self, group):
        saxArray = []
        for seq in group:
            saxArray.append(seq.getWord(self.woordLengte, self.alfabetGrootte))
        return saxArray
    
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
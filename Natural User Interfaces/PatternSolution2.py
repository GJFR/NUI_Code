'''
Created on 10-apr.-2014

@author: Kevin
'''
import DynamicSax
import SeqChecker
import Sequence
import Sequence2
import Visualize
import TimeSequence
import time
class PatternSolution2(object):
    '''
    classdocs
    '''


    def __init__(self, calibrationDict, wordLength, alphabetSize, valuesPerLetter, collisionThreshold, r, heightDifference):
        '''
        Constructor
        '''
        self.dynamicTimeSeqs = { "Left" : DynamicSax.DynamicTimeSeq(wordLength, alphabetSize, collisionThreshold, r, heightDifference) ,
                                 "Right" : DynamicSax.DynamicTimeSeq(wordLength, alphabetSize, collisionThreshold, r, heightDifference) }
        
        self.calibrationDict = calibrationDict
        self.wordLength = wordLength
        self.alphabetSize = alphabetSize
        self.valuesPerLetter = valuesPerLetter
        self.collisionThreshold = collisionThreshold
        self.r = r
        self.heightDifference = heightDifference
        self.labeling = {}
        self.seqChecker = None
        
    def processTimeSequenceCalibration(self):
        calibrationDict = self.calibrationDict
        tijd = time.time()
        self.preprocess(calibrationDict, self.alphabetSize)
        tijd = self.checkpoint("Preprocess: ", tijd)
        
        for direction in calibrationDict:
            print("Start : " + direction)
            dynamicTS = self.dynamicTimeSeqs[direction]
            for i in range(len(calibrationDict[direction])):
                data = calibrationDict[direction][i]
                sequenceGroup = self.makeGroup(data,i)
                tijd = self.checkpoint("Group is made: ", tijd)
                dynamicTS.addSequenceGroup(sequenceGroup)
                tijd = self.checkpoint("Group is done: ", tijd)
            dynamicTS.calculateMotifs()
            tijd = self.checkpoint("Get all motifs: ", tijd)
            dynamicTS.removeCloseMatches()
            tijd = self.checkpoint("Remove close matches: ", tijd)
            #bestMotifs = dynamicTS.getBestMotifs(2)
            #orderedBestMotifs = dynamicTS.orderMotifs(bestMotifs)
            bestMotifs = dynamicTS.getBestMotifs(2)
            orderedBestMotifs = dynamicTS.orderMotifs(bestMotifs)
            tijd = self.checkpoint("Get best motifs: ", tijd)
            
            self.labeling[direction] = orderedBestMotifs
            
            for motif in orderedBestMotifs:
                self.dataPlot(motif, dynamicTS.getMotifs()[motif], direction)
            
    def processTimeSequenceRecognition(self, newSequence):
        if self.seqChecker == None:
            for label in self.labeling:
                for i in range(len(self.labeling[label])):
                    self.labeling[label][i] = self.labeling[label][i].getOriginal()
            self.seqChecker = SeqChecker.SeqChecker(self.labeling, self.wordLength, self.alphabetSize, self.valuesPerLetter, self.collisionThreshold, self.r, self.heightDifference, self.distribution, self.letterWaarden)
        
        return self.seqChecker.checkSequence(newSequence)
        
    
    def preprocess(self, calibrationDict, alphabetSize):
        """concatenate all the data"""
        data = []
        for i in range(len(calibrationDict["Left"])):
            for direction in calibrationDict:
                data.extend(calibrationDict[direction][i])

        """filter seperate sequences and append to one big time sequence"""
        timeSeq = TimeSequence.TimeSequence(data)
        timeSeq.filter()
        self.plotter(timeSeq)
        self.data = timeSeq.getVector()
        dataF = timeSeq.getVector()
    
        
        """Make sax-word and save the distribution for the recognition-fase"""
        timeSeq.makeSaxWord(self.alphabetSize, self.valuesPerLetter)
        self.distribution = timeSeq.getDistribution()
        self.letterWaarden = timeSeq.getLetterWaarden()
        
        for i in range(len(calibrationDict["Left"])):
            for direction in calibrationDict:
                length = len(calibrationDict[direction][i])
                calibrationDict[direction][i] = dataF[:length]
                dataF = dataF[length:]
               
    def makeGroup(self, data, groupNbr):
        sequenceList = []
        sequenceHash = {}
        seqLength = 100
        
        a = len(data) - seqLength
        for j in range(a+1):
            normSeq = Sequence.Sequence(data, j, seqLength).getNormalized()
            sequenceList.append(normSeq)
            sequenceHash[normSeq] = groupNbr
            
        return (sequenceList,sequenceHash)
        
    def checkpoint(self, message, previousTime):
        tijd = time.time()
        print (message + str(tijd - previousTime))
        return tijd
    
    def dataPlot(self, motif, matches, direction):
        print(str(motif) + "  :  " + str(matches))
        Visualize.plot_data5(motif, matches)
    
    def plotter(self, timeSeq):
        timeSeq.makeSaxWord(self.alphabetSize, self.valuesPerLetter)
        Visualize.plot_data_saxString2(timeSeq.getSaxWord())
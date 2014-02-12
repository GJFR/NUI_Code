'''
Created on 9-dec.-2013

@author: Kevin & Gertjan
'''

import Eog
import Sequence
import Visualize
import math
import time

dataStringDict = {'Rechts' : 'Data\\test3_B.csv' , 'Links' : 'Data\\test2_B.csv'}
dataStringRec = 'Data\\test1_B.csv'
verdeelPunten2B = [675,1100,1600,1950,2450]
verdeelPunten4A = [100,500,1050,1450,1900]
verdeelPunten3B = [75,534,1072,1642,2244,2742,3328]
verdeelPuntenDict = {'Rechts' : verdeelPunten3B , 'Links' : verdeelPunten2B }


def IOCalibration(communicationGroups, minSeqLengte, maxSeqLengte, semaphore, direction):
    dataString = dataStringDict[direction]
    data = read(dataString)
    verdeelPunten = verdeelPuntenDict[direction]
    
    for i in range(len(verdeelPunten)-1):
        time.sleep(20)
        sequenceList = []
        sequenceHash = {}
        begin = verdeelPunten[i]
        einde = verdeelPunten[i+1]
        for seqLengte in range(minSeqLengte,maxSeqLengte+1,math.ceil(maxSeqLengte*0.03)):
            a = einde - seqLengte
            for j in range(begin,a+1,2):
                normSeq = Sequence.Sequence(data, j, seqLengte).getNormalized()
                sequenceList.append(normSeq)
                sequenceHash[normSeq] = i
        communicationGroups.put((sequenceList, sequenceHash))
        semaphore.release()

def read(relativePath):
    eog = Eog.Eog(relativePath, 7)
    eog.filter()
    return eog.getMatrix()

def IORecognition(communicationSequences, minSeqLengte, maxSeqLengte, semaphore):
    data = read(dataStringRec)
    print(dataStringRec)
    for einde in range(minSeqLengte,len(data)+1,2):
        for seqLengte in range(minSeqLengte,maxSeqLengte+1,math.ceil(maxSeqLengte*0.03)):
            if einde - seqLengte >= 0:
                normSeq = Sequence.Sequence(data, einde-seqLengte, seqLengte).getNormalized()
                communicationSequences.put(normSeq)
                semaphore.release()
    print("IO-End")
            
def dataPlot(motif, matches, direction):
    print(str(motif) + "  :  " + str(matches))
    Visualize.plot_data4(read(dataStringDict[direction]), motif, matches)

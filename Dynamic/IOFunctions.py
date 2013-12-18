'''
Created on 9-dec.-2013

@author: Kevin & Gertjan
'''

import Eog
import Sequence
import Visualize
import math
import time

def IOCalibration(communicationGroups, minSeqLengte, maxSeqLengte, semaphore):
    data = read('Data\\test2_B.csv')
    verdeelPunten = [675,1100,1600,1950,2450]
    for i in range(len(verdeelPunten)-1):
        time.sleep(20)
        sequenceList = []
        sequenceHash = {}
        begin = verdeelPunten[i]
        einde = verdeelPunten[i+1]
        for seqLengte in range(minSeqLengte,maxSeqLengte+1,math.ceil(maxSeqLengte*0.03)):
            a = einde - seqLengte
            for j in range(begin,a+1):
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
    data = read('Data\\test2_B.csv')
    print("Recognize test2_B")
    for einde in range(minSeqLengte,len(data)+1):
        for seqLengte in range(minSeqLengte,maxSeqLengte+1,math.ceil(maxSeqLengte*0.03)):
            if einde - seqLengte >= 0:
                normSeq = Sequence.Sequence(data, einde-seqLengte, seqLengte).getNormalized()
                communicationSequences.put(normSeq)
                semaphore.release()
    print("IO-End")
            
def dataPlot(motif, matches):
    print(str(motif) + "  :  " + str(matches))
    Visualize.plot_data4(read('Data\\test2_B.csv'), motif, matches)

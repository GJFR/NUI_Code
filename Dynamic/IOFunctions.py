'''
Created on 9-dec.-2013

@author: Gertjan
'''

import Eog
import Sequence
import math
import time

def IOCalibration(communicationGroups, minSeqLengte, maxSeqLengte):
    data = read('Data\\test2_B.csv')
    verdeelPunten = [675,1100,1600,2450]
    for i in range(len(verdeelPunten)-1):
            sequenceHash = {}
            begin = verdeelPunten[i]
            einde = verdeelPunten[i+1]
            for seqLengte in range(minSeqLengte,maxSeqLengte+1,math.ceil(maxSeqLengte*0.03)):
                a = einde - seqLengte
                for j in range(begin,a+1):
                    normSeq = Sequence.Sequence(data, j, seqLengte).getNormalized()
                    sequenceHash[normSeq] = i
            communicationGroups.append(sequenceHash)
            time.sleep(5)

def read(relativePath):
    eog = Eog.Eog(relativePath)
    return eog.getMatrix()

def IORecognition():
    pass
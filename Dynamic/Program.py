'''
Created on 9-dec.-2013

@author: Kevin & Gertjan
'''

import Calibration
import Recognition
import IOFunctions
import Sequence
import math

MIN_SEQ_LENGTH = 100
MAX_SEQ_LENGTH = 150

def initial():
    dataL = IOFunctions.read('Data\\test2_B.csv')
    dataR = IOFunctions.read('Data\\test3_B.csv')
    #return {"Rechts" : [Sequence.Sequence(dataR, 1200, 100).getNormalized(), Sequence.Sequence(dataR, 1982, 100).getNormalized()],
    #        "Links" : [Sequence.Sequence(dataL, 2506, 100).getNormalized(), Sequence.Sequence(dataL, 2672, 100).getNormalized()]}
    return {"Rechts" : [Sequence.Sequence(dataL, 2672, 100).getNormalized(), Sequence.Sequence(dataL, 2506, 100).getNormalized()],
            "Links" : [Sequence.Sequence(dataL, 2506, 100).getNormalized(), Sequence.Sequence(dataL, 2672, 100).getNormalized()]}

def getAllLengths():
    allLengths = []
    for seqLength in range(MIN_SEQ_LENGTH,MAX_SEQ_LENGTH+1,math.ceil(MAX_SEQ_LENGTH*0.1)):
        allLengths.append(seqLength)
    return allLengths

if __name__ == '__main__':
    allLengths = getAllLengths()
    labels = Calibration.run(["Rechts","Links"], allLengths)
    #labels = initial()
    Recognition.recognize(labels, MIN_SEQ_LENGTH, allLengths)

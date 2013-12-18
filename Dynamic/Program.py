'''
Created on 9-dec.-2013

@author: Kevin & Gertjan
'''

import Calibration
import Recognition
import IOFunctions
import Sequence

    
def initial():
    data = IOFunctions.read('Data\\test2_B.csv')
    return {"Rechts" : [Sequence.Sequence(data, 1828, 100).getNormalized(), Sequence.Sequence(data, 1998, 100).getNormalized()]}


if __name__ == '__main__':
    #labels = Calibration.run(["Rechts"])
    labels = initial()
    Recognition.recognize(labels)
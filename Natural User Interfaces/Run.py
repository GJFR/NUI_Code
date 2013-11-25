'''
Created on 18 nov. 2013

@author: Kevin & Gertjan
'''
import Eog
import Sax
import time
import Visualize

def checkpoint(message, previousTime):
    tijd = time.time()
    print (message + str(tijd - previousTime))
    return tijd
    
tijd = time.time()
    
eog1 = Eog.Eog('Data\\test1_A.csv')
eog2 = Eog.Eog('Data\\test1_B.csv')

eog1.filter()
eog2.filter()

eog1.normalize()
eog2.normalize()

tijd = checkpoint("Init: ", tijd)

ts = Sax.TimeSequence(eog2.getMatrix(), 200, 230, 10, 10, 7, 1)

tijd = checkpoint("Create TimeSeq: ", tijd)

colMatrix = ts.getCollisionMatrix()

tijd = checkpoint("Create colMatrix: ", tijd)

goodMatches = ts.calculateGoodMatches(colMatrix)

tijd = checkpoint("calculateGoodMatches: ", tijd)

for motif in goodMatches:
    print (str(motif) + "  :  " + str(goodMatches[motif]))

Visualize.plot_data3(eog1, eog2, goodMatches)

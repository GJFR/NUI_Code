'''
Created on 18 nov. 2013

@author: Kevin & Gertjan
'''
import Eog
import Sax
import time
import Visualize

MIN_SEQ_LENGTH = 100
MAX_SEQ_LENGTH = 150
WORD_LENGTH = 10
ALPHABET_SIZE = 10
COLLISION_THRESHOLD = 7
RANGE = 2
VALUE_A = 0.8
X = 5

def checkpoint(message, previousTime):
    tijd = time.time()
    print (message + str(tijd - previousTime))
    return tijd
    
tijd = time.time()
    
eog1 = Eog.Eog('Data\\test2_A.csv')
eog2 = Eog.Eog('Data\\test2_B.csv')
# verdeelPunten = [0,675,1100,1600,2450,2850,3400]
verdeelPunten = [1600,2500,3400]
eog1.filter()
eog2.filter()

eog1.normalize()
eog2.normalize()

tijd = checkpoint("Init: ", tijd)

ts1 = Sax.TimeSequence(eog2.getMatrix()[1600:], verdeelPunten, MIN_SEQ_LENGTH, MAX_SEQ_LENGTH, WORD_LENGTH, ALPHABET_SIZE, COLLISION_THRESHOLD, RANGE)

tijd = checkpoint("Create TimeSeq: ", tijd)
masks1 = ts1.getMasks()
print (masks1)
tijd = checkpoint("Create masks: ", tijd)
cMatrix1 = ts1.getCollisionMatrix(masks1)
tijd = checkpoint("Create collision matrix: ", tijd)
motifs = ts1.getMotifs(cMatrix1)
tijd = checkpoint("Get all motifs: ", tijd)
motifs = ts1.getTopXMotifs(X, motifs)
tijd = checkpoint("Get top " + str(X) + " of motifs: ", tijd)

for motif in motifs:
    print (str(motif) + "  :  " + str(motifs[motif]))

Visualize.plot_data3(eog1, eog2, motifs, {})

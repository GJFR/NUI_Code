'''
Created on 18 nov. 2013

@author: Kevin & Gertjan
'''
import Eog
import Sax
import time
import Visualize

MIN_SEQ_LENGTH = 200
MAX_SEQ_LENGTH = 230
WORD_LENGTH = 11
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
    
eog1 = Eog.Eog('Data\\test1_A.csv')
eog2 = Eog.Eog('Data\\test1_B.csv')

eog1.filter()
eog2.filter()

eog1.normalize()
eog2.normalize()

tijd = checkpoint("Init: ", tijd)

ts1 = Sax.TimeSequence(eog1.getMatrix(), MIN_SEQ_LENGTH, MAX_SEQ_LENGTH, WORD_LENGTH, ALPHABET_SIZE, COLLISION_THRESHOLD, RANGE)
ts2 = Sax.TimeSequence(eog2.getMatrix(), MIN_SEQ_LENGTH, MAX_SEQ_LENGTH, WORD_LENGTH, ALPHABET_SIZE, COLLISION_THRESHOLD, RANGE)

tijd = checkpoint("Create TimeSeq: ", tijd)
masks1 = ts1.getMasks()
masks2 = ts2.getMasks()
tijd = checkpoint("Create masks: ", tijd)
cMatrix1 = ts1.getCollisionMatrix(masks1)
cMatrix2 = ts2.getCollisionMatrix(masks2)

cMatrix = cMatrix1 + cMatrix2

tijd = checkpoint("Create collision matrix: ", tijd)



motifs1 = ts1.getMotifs(cMatrix1)
motifs2 = ts2.getMotifs(cMatrix2)
tijd = checkpoint("Get all motifs: ", tijd)
motifs1 = ts1.getTopXMotifs(X, motifs1)
tijd = checkpoint("Get top " + str(X) + " of motifs: ", tijd)


for motif in motifs:
    print (str(motif) + "  :  " + str(motifs[motif]))

Visualize.plot_data3(eog1, eog2, motifs)

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
#verdeelPunten = [0,675,1100,1600,2450,2850,3400]
verdeelPunten = [675,1100,1600,2450]
eog1.filter()
eog2.filter()

eog1.normalize()
eog2.normalize()

tijd = checkpoint("Init: ", tijd)

ts1 = Sax.TimeSequence(eog2.getMatrix(), verdeelPunten, MIN_SEQ_LENGTH, MAX_SEQ_LENGTH, WORD_LENGTH, ALPHABET_SIZE, COLLISION_THRESHOLD, RANGE)

tijd = checkpoint("Create TimeSeq: ", tijd)
masks1 = ts1.getMasks()
print (masks1)
tijd = checkpoint("Create masks: ", tijd)
cMatrix1 = ts1.getCollisionMatrix(masks1)
tijd = checkpoint("Create collision matrix: ", tijd)
matchDistPairs = ts1.makeMatchDistancePair(cMatrix1)
tijd = checkpoint("Make match,dist pairs: ", tijd)
matchDistDict = ts1.getMotifs(matchDistPairs)
tijd = checkpoint("Get all motifs: ", tijd)
ts1.removeCloseMatches(matchDistDict)
tijd = checkpoint("Remove close matches: ", tijd)
motif = ts1.getBestMotif(matchDistDict)
tijd = checkpoint("Get best motifs: ", tijd)

motif,matches = motif
print (str(motif) + "  :  " + str(matches))

Visualize.plot_data4(eog1, eog2, motif, matches)


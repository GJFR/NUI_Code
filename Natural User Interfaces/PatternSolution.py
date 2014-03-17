import SaxWord

class PatternSolution(object):
    """description of class"""

    def __init__(self, maxMatchingDistance, alphabetSize, valuesPerLetter, thresholds):
        self.maxMatchingDistance = maxMatchingDistance
        self.alphabetSize = alphabetSize
        self.valuesPerLetter = valuesPerLetter
        self.thresholds = thresholds

    # calibrationDict: een mapping van kijkrichting naar intervallen gehaald uit de calibratie
    # distanceDict: een mapping van sequence naar distance totaal
    def processTimeSequenceCalibration(self, calibrationDict):
        motifDict = {}
        for direction in calibrationDict:
            distanceDict = {}
            for sequence1 in calibrationDict[direction]:
                distanceDict[sequence1] = 0
                for sequence2 in calibrationDict[direction]:
                    if (sequence1 == sequence2):
                        continue
                    distanceDict[sequence1] += sequence1.getHammingDistance(sequence2)
            motifDict[direction] = self.getSmallestDistanceSequence(distanceDict)
        self.motifDict = motifDict
        # print
        print(motifDict["Left"].getWord())

    def processTimesequenceRecognition(self, vector):
        saxWord = SaxWord.SaxWord(vector, alphabetSize, valuesPerLetter, thresholds)
        for direction in motifDict:
            distance = saxWord.getHammingDistance(motifDict[direction])
            if (distance <= self.maxMatchingDistance):
                return direction
        else:
            return None

    def getSmallestDistanceSequence(self, distanceDict):
        smallestDistanceSequence = list(distanceDict.keys())[0]
        for sequence in distanceDict:
            if (distanceDict[sequence] < distanceDict[smallestDistanceSequence]):
                smallesDistanceSequence = sequence
        return smallestDistanceSequence
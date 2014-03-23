import SaxWord

class PatternSolution(object):
    """Attempts to find viewing directions by using patterns."""

    def __init__(self, maxMatchingDistance, alphabetSize, valuesPerLetter, thresholds):
        self.maxMatchingDistance = maxMatchingDistance
        self.alphabetSize = alphabetSize
        self.valuesPerLetter = valuesPerLetter
        self.thresholds = thresholds

    # calibrationDict: een mapping van kijkrichting naar intervallen gehaald uit de calibratie
    # distanceDict: een mapping van sequence naar distance totaal
    def processTimeSequenceCalibration(self, calibrationDict):
        """
        Handles the calibration data by finding the best motif of each direction and putting it in a dictionary motifDict.
        Parameters:
            calibrationDict - dictionairy (direction -> word)
        """
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
        """
        Handles the recoognition by comparing de sax-string of the given vector to the sax-string of the motifs.
        Returns the direction if found, otherwise None.
        Parameters:
            vector          - vector to be compared to the motifs
            alphabetSize    - size of the alphabet for the sax-strings
            valuesPerLetter ...
            TODO persoonlijk vind ik dat die laatste 3 parameters hier niet thuishoren.
            Volgens ons model gebeurt het naar saxstring omzetten al in de preprocessing stap en niet meer in de herkenningsstap
        """
        saxWord = SaxWord.SaxWord(vector, alphabetSize, valuesPerLetter, thresholds)
        for direction in motifDict:
            distance = saxWord.getHammingDistance(motifDict[direction])
            if (distance <= self.maxMatchingDistance):
                return direction
        else:
            return None

    def getSmallestDistanceSequence(self, distanceDict):
        """
        Returns the sequence with the smallest distance.
        Parameters:
            distancDist - dictionary (sequence -> total distance to other sequences)
        """
        smallestDistanceSequence = list(distanceDict.keys())[0]
        for sequence in distanceDict:
            if (distanceDict[sequence] < distanceDict[smallestDistanceSequence]):
                smallesDistanceSequence = sequence
        return smallestDistanceSequence
import SaxWord
import Visualize
import TimeSequence

class PatternSolution(object):
    """Attempts to find viewing directions by using patterns."""

    def __init__(self, maxMatchingDistance, alphabetSize, valuesPerLetter):
        self.maxMatchingDistance = maxMatchingDistance
        self.alphabetSize = alphabetSize
        self.valuesPerLetter = valuesPerLetter

        
    # calibrationDict: een mapping van kijkrichting naar intervallen gehaald uit de calibratie
    # distanceDict: een mapping van sequence naar distance totaal
    def processTimeSequenceCalibration(self, calibrationDict):
        """
        Handles the calibration data by finding the best motif of each direction and putting it in a dictionary motifDict.
        Parameters:
            calibrationDict - dictionairy (direction -> sequentie)
        """
        """concatenate all the data"""
        data = []
        for i in range(len(calibrationDict["Left"])):
            for direction in calibrationDict:
                data.extend(calibrationDict[direction][i])
        
        """find the thresholds"""
        timeSeq = TimeSequence.TimeSequence(data)
        timeSeq.filter()
        timeSeq.makeSaxWord(self.alphabetSize, self.valuesPerLetter)
        saxWord = timeSeq.getSaxWord()
        self.thresholds = saxWord.getThresholds()
        
        """make saxWords for each sequence"""
        calibrationWordDict = {}
        for direction in calibrationDict:
            calibrationWordDict[direction] = []
            for seq in calibrationDict[direction]:
                calibrationWordDict[direction].append(SaxWord.SaxWord(seq,self.alphabetSize,self.valuesPerLetter,self.thresholds, timeSeq.getLetterWaarden()))
        
        """compare all the saxWords of the same direction with each other"""
        motifDict = {}
        for direction in calibrationWordDict:
            distanceDict = {}
            for sequence1 in calibrationWordDict[direction]:
                distanceDict[sequence1] = 0
                for sequence2 in calibrationWordDict[direction]:
                    if (sequence1 == sequence2):
                        continue
                    distanceDict[sequence1] += sequence1.getHammingDistance(sequence2)
            motifDict[direction] = self.getSmallestDistanceSequence(distanceDict)
        self.motifDict = motifDict
        # print
        print(motifDict["Left"].getWord())
        print(motifDict["Right"].getWord())
        
        """Print all the sequences"""
        for direction in calibrationDict:
            for seq in calibrationDict[direction]:
                sequence = TimeSequence.TimeSequence(seq)
                sequence.filter()
                sequence.makeSaxWord(self.alphabetSize, self.valuesPerLetter,self.thresholds, timeSeq.getLetterWaarden())
                Visualize.plot_data_saxString(sequence, self.alphabetSize, self.valuesPerLetter)
        
        """Print the concatenated data"""
        Visualize.plot_data_saxString(timeSeq, self.alphabetSize, self.valuesPerLetter)

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
        saxWord = SaxWord.SaxWord(vector, self.alphabetSize, self.valuesPerLetter, self.thresholds)
        for direction in self.motifDict:
            distance = saxWord.getHammingDistance(self.motifDict[direction])
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
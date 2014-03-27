import SaxWord
import Visualize
import TimeSequence

class PatternSolution(object):
    """Attempts to find viewing directions by using patterns."""

    def __init__(self, calibrationDict, alphabetSize, valuesPerLetter, maxMatchingDistance):
        self.maxMatchingDistance = maxMatchingDistance
        self.preprocess(calibrationDict, valuesPetLetter)

        
    # calibrationDict: een mapping van kijkrichting naar intervallen gehaald uit de calibratie
    # distanceDict: een mapping van sequence naar distance totaal
    def processTimeSequenceCalibration(self, calibrationDict):
        """
        Handles the calibration data by finding the best motif of each direction and putting it in a dictionary motifDict.
        Parameters:
            calibrationDict - dictionairy (direction -> sequentie)
        """
       
        
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

    def processTimesequenceRecognition(self, saxWord):
        """
        Handles the recoognition by comparing de sax-string of the given vector to the sax-string of the motifs.
        Returns the direction if found, otherwise None.
        Parameters:
            saxWord         - sax word to be compared to the motifs
        """
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

    def preprocess(calibrationDict, alphabetSize, valuesPerLetter):
         """concatenate all the data"""
         data = []
         for i in range(len(calibrationDict["Left"])):
           for direction in calibrationDict:
               data.extend(calibrationDict[direction][i])

         """find the thresholds"""
         timeSeq = TimeSequence.TimeSequence(data)
         timeSeq.filter()
         timeSeq.makeSaxWord(alphabetSize, valuesPerLetter)
         saxWord = timeSeq.getSaxWord()
         self.thresholds = saxWord.getDistribution()
        
         """make saxWords for each sequence"""
         self.calibrationWordDict = {}
         for direction in calibrationDict:
             self.calibrationWordDict[direction] = []
             for seq in calibrationDict[direction]:
                 self.calibrationWordDict[direction].append(SaxWord.SaxWord(seq,alphabetSize,valuesPerLetter,thresholds, timeSeq.getLetterWaarden()))

         self.plotter(timeSeq, alphabetSize, valuesPerLetter)

    def plotter(timeSeq, alphabetSize, valuesPerLetter):
        """Print all the sequences"""
        for direction in self.calibrationWordDict:
            for word in self.calibrationWordDict[direction]:
                Visualize.plot_data_saxString2(word)
        
        """Print the concatenated data"""
        Visualize.plot_data_saxString(timeSeq, alphabetSize, valuesPerLetter)
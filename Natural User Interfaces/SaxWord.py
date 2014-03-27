import math

class SaxWord(object):
    """Sax word"""

    def __init__(self, vector, alphabetSize, valuesPerLetter, distribution=None, letterWaarden=None):
        
        self.vector = vector
        self.alphabetSize = alphabetSize
        self.valuesPerLetter = valuesPerLetter
        self.alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        sortedVector = sorted(vector)
        if distribution == None:
            self.distribution = []
            self.makeDistribution(sortedVector)
        else:
            self.distribution = distribution
        self.word = ""
        self.makeWord()
        if letterWaarden == None:
            self.letterWaarden = {}
            self.makeLetterwaarden(sortedVector)
        else:
            self.letterWaarden = letterWaarden

    def getVector(self):
        return self.vector

    def getWord(self):
        return self.word;

    def getDistribution(self):
        return self.distribution

    def getLetterWaarden(self):
        return self.letterWaarden

    def getHammingDistance(self, other):
        """
        Calculates the hamming distance between this sax word and the other sax word.
        Parameters:
            other   - the other sax word
        Returns:
            the distance between this sax word and the other sax word
        """
        distance = 0
        for i in range(len(self.word)):
            letter1 = self.getWord()[i]
            letter2 = other.getWord()[i]
            distance = distance + self.getHamming(letter1, letter2)
        return distance

    def getHamming(self, letter1, letter2):
        """
        Returns 1 if the two given letters are different, otherwise false.
        """
        if (letter1 != letter2):
            return 1
        else:
            return 0

    def makeDistribution(self, sortedVector):
        """
        Assigns thresholds to letters. This is used to make the sax word.
        Parameters:
            sortedVector    - the sorted vector
        """
        self.distribution.append(sortedVector[0])
        for index in range(1,self.alphabetSize + 1):
            positie = math.floor(index * len(sortedVector)/self.alphabetSize)-1
            self.distribution.append(sortedVector[positie])

    def makeWord(self):
        """
        Makes the actual sax word.
        """
        saxWord = ""
        for index in range(0,len(self.vector) - self.valuesPerLetter,self.valuesPerLetter):
            total = 0
            for j in range(self.valuesPerLetter):
                total = total + self.vector[index+j]
            average = total / self.valuesPerLetter
            for j in range(1,self.alphabetSize + 1):
                if average < self.distribution[j]:
                    saxWord = saxWord + self.alphabet[j - 1]
                    break
            else:
                saxWord = saxWord + self.alphabet[self.alphabetSize-1]
        self.word = saxWord

    def makeLetterwaarden(self, sortedVector):
        """
        Assigns a value to each letter. This is used primarily to visualize the sax words.
        Parameters:
            sortedVector    - the sorted vector
        """
        posities = [0]
        for index in range(1,self.alphabetSize+1):
            posities.append(math.floor(index * len(sortedVector)/self.alphabetSize)-1)
        for index in range(len(posities) - 1):
            total = 0
            for pos in range(posities[index], posities[index+1]):
                total = total + sortedVector[pos]
            mean = total / (posities[index+1] - posities[index])
            self.letterWaarden[self.alphabet[index]] = mean
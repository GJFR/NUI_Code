class SaxWord(object):
    """description of class"""

    def __init__(self, vector, alphabetSize, valuesPerLetter, thresholds):
        self.word = ""
        self.vector = vector
        self.alphabetSize = alphabetSize
        self.valuesPerLetter = valuesPerLetter
        self.thresholds = thresholds
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.makeSaxWord()

    def getWord(self):
        return self.word;

    def getHammingDistance(self, other):
        distance = 0
        for i in range(len(self.word)):
            letter1 = self.getWord()[i]
            letter2 = other.getWord()[i]
            distance = distance + self.getHamming(letter1, letter2)
        return distance

    def getHamming(self, letter1, letter2):
        if (letter1 != letter2):
            return 1
        else:
            return 0

    def makeSaxWord(self):
        saxWord = ""
        for index in range(0,len(self.vector) - self.valuesPerLetter,self.valuesPerLetter):
            total = 0
            for j in range(self.valuesPerLetter):
                total = total + self.vector[index+j]
            average = total / self.valuesPerLetter
            for j in range(1,self.alphabetSize + 1):
                if average < self.thresholds[j]:
                    saxWord = saxWord + self.alphabet[j - 1]
                    break
            else:
                saxWord = saxWord + self.alphabet[self.alphabetSize-1]
        self.word = saxWord
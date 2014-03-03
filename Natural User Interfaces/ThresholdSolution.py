class ThresholdSolution(object):
    
     def __init__(self, timeSeq, threshold_dict, minimumLength):
         self.timeSeq = timeSeq
         self.threshold_dict = threshold_dict
         self.minimumLength = minimumLength
         

     def processTimeSequence(self):
        counterLeft = 0
        counterRight = 0
        hasDirection = False
        saxString = self.timeSeq.getSaxString()
        for index in range(len(saxString)):
            if saxString[index] < self.threshold_dict["Left"]:
                counterLeft = counterLeft + 1
            elif saxString[index] > self.threshold_dict["Right"]:
                counterRight = counterRight + 1
            else:
                counterLeft = 0
                counterRight = 0
                hasDirection = False
            if counterLeft >= self.minimumLength and hasDirection == False:
                print(str(index * self.timeSeq.waardesPerLetter) + ": Left")
                hasDirection = True
            if counterRight >= self.minimumLength and hasDirection == False:
                print(str(index * self.timeSeq.waardesPerLetter) + ": Right")
                hasDirection = True
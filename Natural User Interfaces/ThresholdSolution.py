class ThresholdSolution(object):
    
     def __init__(self, directionThresholds, minimalThresholdHits):
         self.threshold_dict = directionThresholds
         self.minimalThresholdHits = minimalThresholdHits
         self.counterLeft = 0
         self.counterRight = 0
         self.hasDirection = False

     def processTimeSequenceCalibration(self, timeSeq):
        counterLeft = 0
        counterRight = 0
        hasDirection = False
        saxString = timeSeq.getSaxString()
        for index in range(len(saxString)):
            if saxString[index] < self.threshold_dict["Left"]:
                counterLeft = counterLeft + 1
            elif saxString[index] > self.threshold_dict["Right"]:
                counterRight = counterRight + 1
            else:
                counterLeft = 0
                counterRight = 0
                hasDirection = False
            if counterLeft >= self.minimalThresholdHits and hasDirection == False:
                print(str(index * timeSeq.waardesPerLetter) + ": Left")
                hasDirection = True
            if counterRight >= self.minimalThresholdHits and hasDirection == False:
                print(str(index * timeSeq.waardesPerLetter) + ": Right")
                hasDirection = True

     def processTimeSequenceRecognition(self, letter):
         if letter < self.threshold_dict["Left"]:
            self.counterLeft = self.counterLeft + 1
         elif letter > self.threshold_dict["Right"]:
            self.counterRight = self.counterRight + 1
         else:
            self.counterLeft = 0
            self.counterRight = 0
            self.hasDirection = False
         if self.counterLeft >= self.minimalThresholdHits and self.hasDirection == False:
            print(": Left")
            self.hasDirection = True
         if self.counterRight >= self.minimalThresholdHits and self.hasDirection == False:
            print(": Right")
            self.hasDirection = True

     """Returns boolean die zegt ofdat een threshold is gebroken of niet."""
     def processTimeSequenceRecognition2(self, letter):
         if letter < self.threshold_dict["Left"]:
            self.counterLeft = self.counterLeft + 1
         elif letter > self.threshold_dict["Right"]:
            self.counterRight = self.counterRight + 1
         else:
            self.counterLeft = 0
            self.counterRight = 0
            self.hasDirection = False
            return False
         if self.counterLeft >= self.minimalThresholdHits and self.hasDirection == False:
            print(": Left")
            self.hasDirection = True
         if self.counterRight >= self.minimalThresholdHits and self.hasDirection == False:
            print(": Right")
            self.hasDirection = True
         return True
class ThresholdSolution(object):
     """Attempts to find viewing directions by using thresholds."""

     def __init__(self, directionThresholds, minimalThresholdHits):
         self.threshold_dict = directionThresholds
         self.minimalThresholdHits = minimalThresholdHits
         self.counterLeft = 0
         self.counterRight = 0
         self.hasDirection = False

     
     #TODO
     #Het enige nut van deze methode is het nakijken of de calibratie wel goed gebeurd is.
     #Later als we een echte calibratie reeks van kijkrichtingen hebben, kunnen we die meegeven en checken of ze er mee overeen komen?
     def processTimeSequenceCalibration(self, timeSeq):
        counterLeft = 0
        counterRight = 0
        hasDirection = False
        saxString = timeSeq.getSaxWord().getWord()
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
                print(str(index * timeSeq.getSaxWord().valuesPerLetter) + ": Left")
                hasDirection = True
            if counterRight >= self.minimalThresholdHits and hasDirection == False:
                print(str(index * timeSeq.getSaxWord().valuesPerLetter) + ": Right")
                hasDirection = True

     def processTimeSequenceRecognitionNoBoolean(self, letter):
         """
         Handles incoming letters by checking if a threshold is broken for a predefined number of times.
         Parameters:
            letter  - letter to analyse
         """
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
     def processTimeSequenceRecognition(self, letter):
         if letter < self.threshold_dict["Left"]:
            self.counterLeft = self.counterLeft + 1
         elif letter > self.threshold_dict["Right"]:
            self.counterRight = self.counterRight + 1
         else:
            if self.hasDirection:
                print(": End")
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
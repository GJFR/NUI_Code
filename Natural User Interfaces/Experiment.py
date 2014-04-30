'''
Created on 20-apr.-2014

@author: Kevin
'''
import EyeTracker
    
def thresholdExperiment():
    
    
    calibrationComp2 = ('Data2\\test8_B.csv',0,3400)
    calibrationComp3 = ('Data2\\test9_B.csv',0,3740)

    
    
    recognitionComp3 = ('Data2\\test2_B.csv',900,3500) #4 links
    recognitionComp4 = ('Data2\\test3_B.csv',0,3500)# 6 links
    recognitionComp5 = ('Data2\\test4_B.csv',0,3700)# 6 rechts
    recognitionComp6 = ('Data2\\test5_B.csv',0,3730)#6 links
    recognitionComp7 = ('Data2\\test6_B.csv',390,3700)#6 rechts
    
    recognitionComp9 = ('Data2\\test31_B.csv',0,4800)
    
    recognitionComp10 = ('Data2\\test30_B.csv',0,4800)
    EyeTracker.runT(calibrationComp3, recognitionComp10)
    
    
    
    
    
    
    calibrationComp1 = ('Data\\test1_B.csv',330,2100)
    calibrationComp2 = ('Data2\\test8_B.csv',0,3400)
    calibrationComp3 = ('Data2\\test9_B.csv',0,3740)
    calibrationComp4 = ('Data2\\test24_B.csv',0,4900)
    
   
    
    
    recognitionComp1 = ('Data\\test2_B.csv',0,3400)
    recognitionComp2 = ('Data\\test3_B.csv',0,3500)
    recognitionComp3 = ('Data2\\test2_B.csv',400,3500)
    recognitionComp4 = ('Data2\\test3_B.csv',0,3500)
    recognitionComp5 = ('Data2\\test4_B.csv',0,3700)
    recognitionComp6 = ('Data2\\test5_B.csv',0,3730)
    recognitionComp7 = ('Data2\\test6_B.csv',390,3700)
    recognitionComp8 = ('Data2\\test26_B.csv',0,4980)
    recognitionComp9 = ('Data2\\test31_B.csv',0,4800) #snelle
    recognitionComp10 = ('Data2\\test30_B.csv',0,4800) #snelle
    recognitionComp11 = ('Data3\\test001_B.csv',0,4800)
    recognitionComp12 = ('Data3\\test002_B.csv',0,4980) #weinig + kort
    recognitionComp13 = ('Data3\\test005_B.csv',0,4900)
    
    #EyeTracker.runT(calibrationComp3, recognitionComp5)
    
    
    

if __name__ == '__main__':
    thresholdExperiment()
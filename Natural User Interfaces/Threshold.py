'''
Created on 6-nov.-2013

@author: Gertjan & Kevin
'''

global thresholdLeft
global thresholdRight
global thresholdDown
global thresholdUp
global occurringType
global counter

def processData(eog):
    global occurringType
    global counter
    occurringType = 'none'
    counter = 1
    for x in range(0, len(eog)-1):
        receiveDatapoints(eog[x],eog[x+1])
        if (counter == 5):
            print(occurringType + str(x))

def receiveDatapoints(x,y):
    global occurringType
    global counter
    if (x - y > 0.025):
        currentType = 'descent'
    elif (x - y < -0.025):
        currentType = 'ascent'
    else:
        currentType = 'none'
        
    if (currentType == occurringType):
        counter += 1
    else:
        occurringType = currentType
        counter = 1
    
def breakThreshold(x):
    global thresholdLeft
    global thresholdRight
    if (x < thresholdLeft):
        return 'left'
    if (x > thresholdRight):
        return 'right'
    return None

def setThresholdDifference(type,value):
    global thresholdLeft
    global thresholdRight
    global thresholdDown
    global thresholdUp
    if (type == 'left'):
        thresholdLeft = value
    if (type == 'right'):
        thresholdRight = value
    if (type == 'down'):
        thresholdDown = value
    if (type == 'up'):
        thresholdUp = value
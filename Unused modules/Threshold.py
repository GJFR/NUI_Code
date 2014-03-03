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
    matrix = eog.getMatrix()
    occurringType = 'n'
    counter = 1
    for x in range(0, len(matrix)-3):
        receiveDatapoints(matrix[x],matrix[x+3])
        if (counter == 3):
            print(occurringType + str(x))
            eog.addAnnotation([occurringType,(x,matrix[x])])

def receiveDatapoints(x,y):
    global occurringType
    global counter
    if (x - y > 0.1):
        currentType = 'd'
    elif (x - y < -0.1):
        currentType = 'a'
    else:
        currentType = 'n'
        
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

def setThresholdDifference(direction,value):
    global thresholdLeft
    global thresholdRight
    global thresholdDown
    global thresholdUp
    if (direction == 'left'):
        thresholdLeft = value
    if (direction == 'right'):
        thresholdRight = value
    if (direction == 'down'):
        thresholdDown = value
    if (direction == 'up'):
        thresholdUp = value
'''
Created on 29-apr.-2014

@author: Kevin
'''


import socket
import matplotlib.pyplot as plt
from time import sleep
import threading

HOST = 'localhost'
PORT = 42001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def read_from_port1(amount):
    runQueue1 = []
    
    for i in range(amount):
        
        data = ""
        size = int.from_bytes(s.recv(4), byteorder = "big")
        
        data = str(s.recv(size), encoding = "UTF-8")
        if ("eogDongle" in data):
            value = int(data[28:])
        else:
            continue
        
        
        try:
            channel = int(data[26:27])
            waarde = value
        
            if channel == 1:
                print(waarde)
                runQueue1.append(waarde)
        except ValueError:
            print(data)
    return runQueue1

def read_from_port2(runQueue1, runLock1):
    global eog
    
    eog = 1000 * [500]
    
    while True:
        data = ""
        size = int.from_bytes(s.recv(4), byteorder = "big")
        
        data = str(s.recv(size), encoding = "UTF-8")
        if ("eogDongle" in data):
            value = int(data[28:])
        else:
            continue
        
        
        try:
            channel = int(data[26:27])
            waarde = value
            
            if channel == 1:
                #print("add")
                #print(waarde)
                eog[0:999] = eog[1:1000]
                eog[999] = waarde
                
                if runLock1.acquire(False):
                    #print("acqueired")
                    runQueue1.put(waarde)
                    runLock1.release()
                    #print("released")
        except ValueError:
            print(data)

def plot_data(dataWindow):
    global eog
    print("Init plotting")
    #   b, a = butter(2, 0.0001, 'high')
    #b, a = butter(2, 0.5, 'high')
    
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    line1, = ax1.plot(eog)
    line2, = ax2.plot(dataWindow.filt_data)
    #line2, = ax2.plot(eog2)
    fig.show()
    
    print("Start plotting")
    
    #while True:
    for t in range(40*12):
    
        #print("Filtering")
        #eog1_filt = filtfilt(b, a, eog1)
        #eog2_filt = filtfilt(b, a, eog2)
        
        #print("Plotting")
        #ax1.set_ylim((min(eog1_filt), max(eog1_filt)))
        ax1.set_ylim(0,1000)
        ax2.set_ylim(-500,500)
        line1.set_ydata(eog)
        line2.set_ydata(dataWindow.filt_data)
        #ax2.set_ylim((min(eog2_filt), max(eog2_filt)))

        fig.canvas.draw()
        fig.show()
        
        sleep(.5)


def run(amount):
    return read_from_port1(amount)

def run2(runQueue1, runLock1, dataWindow):
    thread = threading.Thread(target=plot_data, args= (dataWindow,))
    thread.start()
    read_from_port2(runQueue1, runLock1)
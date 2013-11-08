'''
Created on 22-okt.-2013

@author: Gertjan & Kevin
'''

import csv

import io
import serial
import threading
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import Threshold
from scipy.signal import filtfilt, butter
from time import sleep
from struct import *

global eog1
global eog2
global eog1_filt
global eog2_filt


with open('C:\\Users\\Gertjan\\git\\NUI_Code\\Data\\test10_A.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        eog1 = [float(i) for i in row]
        print(eog1)
        
with open('C:\\Users\\Gertjan\\git\\NUI_Code\\Data\\test10_B.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        eog2 = [float(i) for i in row]
        print(eog2)

print(eog1)
eog1_filt = np.zeros(len(eog1))
eog2_filt = np.zeros(len(eog2))

b, a = butter(2, 0.5, 'low')

eog1_filt = filtfilt(b, a, eog1)
eog2_filt = filtfilt(b, a, eog2)

def normalize(dataset):
    mean = sum(dataset)/len(dataset)
    dataset = dataset - mean
    dataset = dataset/abs(dataset).max()
    return dataset

eog1_n = normalize(eog1_filt)
eog2_n = normalize(eog2_filt)

def plot_data():
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    line1, = ax1.plot(eog1_n)
    line2, = ax2.plot(eog2_n)
    plt.show()
    
plot_data()

Threshold.setThresholdDifference('left', -0.6)
Threshold.setThresholdDifference('right', 0.6)
Threshold.setThresholdDifference('down', 15000)
Threshold.setThresholdDifference('up', -7000)


Threshold.processData(eog2_n)
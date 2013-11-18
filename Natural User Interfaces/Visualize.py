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
import Eog
import Sax
from scipy.signal import filtfilt, butter
from time import sleep
from struct import *
import os

global eog1
global eog2
global eog1_filt
global eog2_filt

path = (os.getcwd()[:len(os.getcwd()) - 23])

with open(path + 'Data\\test2_A.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data1 = [float(i) for i in row]
        
with open(path + 'Data\\test2_B.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data2 = [float(i) for i in row]


b, a = butter(2, 0.05, 'low')
data1 = filtfilt(b, a, data1)
data2 = filtfilt(b, a, data2)

eog1 = Eog.Eog(data1)
eog2 = Eog.Eog(data2)

eog1.normalize()
eog2.normalize()

ts2 = Sax.TimeSequence(eog2.getMatrix(), 250, 6, 10, 3, 1)
goodMatches = ts2.calculateGoodMatches(ts2.getCollisionMatrix())
print (goodMatches)


def plot_data():
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.plot(eog1.getMatrix())
    ax2.plot(eog2.getMatrix())
    for annotation in eog1.getAnnotations():
        ax1.annotate(annotation[0], xy = annotation[1], xycoords = 'data', xytext = annotation[1], textcoords = 'data')
        print(annotation[0])
    for annotation in eog2.getAnnotations():
        ax2.annotate(annotation[0], xy = annotation[1], xycoords = 'data', xytext = annotation[1], textcoords = 'data')
        print(annotation[0])
    plt.show()

def plot_data2(sequenceList):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    line1, = ax1.plot(eog1.getMatrix())
    line2, = ax2.plot(eog2.getMatrix())
    for sequence in sequenceList:
        ax2.plot(range(sequence.start, sequence.start + sequence.length), sequence.getAllPoints(), color = 'r')
    plt.show()

def plot_data3(diction):
    for motif in diction:
        fig = plt.figure()
        '''ax1 = fig.add_subplot(211)'''
        ax2 = fig.add_subplot(212)
        '''line1, = ax1.plot(eog1.getMatrix())'''
        line2, = ax2.plot(eog2.getMatrix())
        ax2.plot(range(motif.start, motif.start + motif.length), motif.getAllPoints(), color = 'g')
        for sequence in diction[motif]:
            ax2.plot(range(sequence.start, sequence.start + sequence.length), sequence.getAllPoints(), color = 'r')
        plt.show()

plot_data3(goodMatches)
'''
Threshold.setThresholdDifference('left', -0.6)
Threshold.setThresholdDifference('right', 0.6)
Threshold.setThresholdDifference('down', 15000)
Threshold.setThresholdDifference('up', -7000)

'''
'''Threshold.processData(eog1)
Threshold.processData(eog2)'''
'''plot_data()'''

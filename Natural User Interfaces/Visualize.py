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

def plot_data3(eog1, eog2, diction):
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

'''
Threshold.setThresholdDifference('left', -0.6)
Threshold.setThresholdDifference('right', 0.6)
Threshold.setThresholdDifference('down', 15000)
Threshold.setThresholdDifference('up', -7000)

'''
'''Threshold.processData(eog1)
Threshold.processData(eog2)'''
'''plot_data()'''

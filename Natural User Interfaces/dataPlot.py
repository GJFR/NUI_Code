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
import TimeSequence
import Sax
import os
from scipy.signal import filtfilt, butter
from time import sleep
from struct import *

global timeSeq1
global timeSeq2
global timeSeq1_filt
global timeSeq2_filt

aantalLetters = 8
waardesPerLetter = 15

path = 'Data2\\test33_B.csv'



timeSeq1 = TimeSequence.TimeSequence(path,23, aantalLetters, waardesPerLetter)
timeSeq1f = TimeSequence.TimeSequence(path,23, aantalLetters, waardesPerLetter)

#timeSeq1.normalize()
#timeSeq1f.normalize()

timeSeq1f.filter()

def plot_data():
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    line1, = ax1.plot(timeSeq1.getMatrix())
    ax1.plot(timeSeq1f.getMatrix())
    line2, = ax2.plot(timeSeq1.getMatrix() - timeSeq1f.getMatrix())
    plt.show()

plot_data()

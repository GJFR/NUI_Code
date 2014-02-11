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
import os
from scipy.signal import filtfilt, butter
from time import sleep
from struct import *

global eog1
global eog2
global eog1_filt
global eog2_filt

eog1 = Eog.Eog('Data\\test3_B.csv',23)
eog1f = Eog.Eog('Data\\test3_B.csv',23)


eog1.normalize()
eog1f.normalize()

eog1f.filter()

def plot_data():
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    line1, = ax1.plot(eog1.getMatrix())
    line2, = ax2.plot(eog1f.getMatrix())
    plt.show()

plot_data()

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

def readData(relativePath, nbr):
        path = (os.getcwd()[:len(os.getcwd())])

        with open(path + "\\" + relativePath) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                return [float(i) for i in row]

aantalLetters = 8
waardesPerLetter = 15

path = 'PosterData\\test006_B.csv'
path2 = 'PosterData\\test006_B.csv'


matrix = readData(path, 23)[:4900]
#matrix.extend(readData(path2, 23))
matrix2 = np.zeros(4900)

for i in range(len(matrix)):
    matrix2[i] = matrix[i] - 6*i

timeSeq1 = TimeSequence.TimeSequence(matrix2, aantalLetters, waardesPerLetter)
timeSeq1f = TimeSequence.TimeSequence(matrix2, aantalLetters, waardesPerLetter)

#timeSeq1.normalize()
#timeSeq1f.normalize()

timeSeq1f.filter()



def plot_data():
    fig = plt.figure()
    #ax1 = fig.add_subplot(111)
    plt.xlim(0, 4900)
    plt.ylim(-40000,40000)
    
    ax2 = fig.add_subplot(111)
    ax2.tick_params(axis='both', labelsize=36)
    #ax1.plot(timeSeq1.getMatrix())
    
    plt.ylim(-40000,40000)
    plt.xlim(0, 4900)
    lines2 = ax2.plot(timeSeq1f.getMatrix())
    plt.setp(lines2, linewidth=2)
    plt.xlim(0, 4900)
    plt.ylim(-40000,40000)
    plt.show()

plot_data()

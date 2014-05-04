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
import Visualize
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

path = 'Data2\\test20_B.csv'
path2 = 'PosterData\\test006_B.csv'


matrix = readData(path, 23)[1500:2100]
#matrix.extend(readData(path2, 23))
matrix2 = matrix

#for i in range(len(matrix)):
#    matrix2[i] = matrix[i] - 6*i

timeSeq1 = TimeSequence.TimeSequence(matrix2)
timeSeq1f = TimeSequence.TimeSequence(matrix2)

#timeSeq1.normalize()
#timeSeq1f.normalize()



timeSeq1f.filter()

#sorted_vector = sorted(timeSeq1f.getVector())


alphabetSize = 8
valuesPerLetter = 15

timeSeq1f.makeSaxWord(alphabetSize, valuesPerLetter)
#Visualize.plot_data_saxString2(timeSeq1f.getSaxWord())



def plot_data(vector, filt_vector):
    fig = plt.figure()
    #ax1 = fig.add_subplot(111)
    #plt.xlim(0, 4900)
    #plt.ylim(-40000,40000)
    ax1 = fig.add_subplot(111)
    #ax2 = fig.add_subplot(212)
    ax1.tick_params(axis='both', labelsize=36)
    #ax1.plot(timeSeq1.getMatrix())
    
    #ax2.add_line(plt.axhline(y=26200, color = 'r'))
    #ax2.add_line(plt.axhline(y=26200 * 0.5, color = 'g'))
    #ax2.add_line(plt.axhline(y=-28600, color = 'r'))
    #ax2.add_line(plt.axhline(y=-28600 * 0.5, color = 'g'))

    #plt.ylim(-40000,40000)
    #plt.xlim(0, 4900)
    #lines2 = ax2.plot(vector)
    lines1 = ax1.plot(vector, color = 'b')
    lines2 = ax1.plot(filt_vector, color = 'r')
    plt.setp(lines1, linewidth=2)
    plt.setp(lines2, linewidth=2)
    #plt.xlim(0, 4900)
    #plt.ylim(-40000,40000)
    plt.show()

def plot_data3(vector):
    fig = plt.figure()
    
    ax2 = fig.add_subplot(111)
    ax2.tick_params(axis='both', labelsize=36)
    lines2 = ax2.plot(timeSeq1f.getVector(), color = 'b')
    lines3 = ax2.plot(range(120,220), timeSeq1f.getVector()[120:220], color = 'r')
    #plt.ylim(-30000,30000)
    plt.setp(lines2, linewidth=2)
    plt.setp(lines3, linewidth=2)
    plt.show()

def plot_data2(vector, saxWord):


    fig = plt.figure()
    plt.xlim(0, 4900)
    plt.ylim(-40000,40000)
    
    ax2 = fig.add_subplot(111)

    ax2.tick_params(axis='both', labelsize=36)
    
    start = 0.125 * len(vector)
    for i in range(1,len(saxWord.getDistribution()) - 1):
        threshold = saxWord.getDistribution()[i]
        ax2.add_line(plt.axhline(y=threshold, color = 'r'))
        ax2.axvline(x=start, ymin=0, ymax=1, color = 'r')
        start = start + (0.125 * len(vector))
    
    plt.ylim(-40000,40000)
    plt.xlim(0, 4900)
    lines2 = ax2.plot(vector, color = 'b')
    plt.setp(lines2, linewidth=2)
    plt.xlim(0, 4900)
    plt.ylim(-40000,40000)
    plt.show()

#plot_data(timeSeq1.getVector(), timeSeq1f.getVector())

plot_data3(timeSeq1f.getVector())

#plot_data2(sorted_vector,timeSeq1f.getSaxWord())
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
import ThresholdSolution
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
        ax2.plot(range(sequence.getStart(), sequence.getStart() + sequence.getLength()), sequence.getAllPoints(), color = 'r')
    plt.show()

def plot_data3(eog1, eog2, diction1, diction2):
    fig = plt.figure()
    for motif in diction1:
        ax1 = fig.add_subplot(211)
        line1, = ax1.plot(eog1.getMatrix())
        ax1.plot(range(motif.getStart(), motif.getStart() + motif.getLength()), motif.getOriginal().getAllPoints(), color = 'g')
        for sequence in diction1[motif]:
            ax1.plot(range(sequence.getStart(), sequence.getStart() + sequence.getLength()), sequence.getOriginal().getAllPoints(), color = 'r')
        plt.show()
    for motif in diction2:
        ax2 = fig.add_subplot(212)
        line2, = ax2.plot(eog2.getMatrix())
        ax2.plot(range(motif.getStart(), motif.getStart() + motif.getLength()), motif.getOriginal().getAllPoints(), color = 'g')
        for sequence in diction2[motif]:
            ax2.plot(range(sequence.getStart(), sequence.getStart() + sequence.getLength()), sequence.getOriginal().getAllPoints(), color = 'r')
        plt.show()
        
def plot_data4(data2, motif, matches):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    line1, = ax1.plot(data2)
    ax1.plot(range(motif.getStart(), motif.getStart() + motif.getLength()), motif.getOriginal().getAllPoints(), color = 'g')
    for sequence,dist in matches:
        ax1.plot(range(sequence.getStart(), sequence.getStart() + sequence.getLength()), sequence.getOriginal().getAllPoints(), color = 'r')
    plt.show()
    
def plot_data_saxString(timeSeq,aantal,waardesPerLetter):
    saxToMatrix = []
    for letter in timeSeq.getSaxString():
        '''waarde = (eog.getThresholds()[letterIndex] + eog.getThresholds()[letterIndex+1]) / 2'''
        waarde = timeSeq.getLetterWaarden()[letter]
        for i in range(waardesPerLetter):
            saxToMatrix.append(waarde)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(timeSeq.getMatrix())
    ax1.plot(saxToMatrix, color = 'g')
    for threshold in timeSeq.getThresholds():
        ax1.add_line(plt.axhline(y=threshold, color = 'r'))

    ax2 = fig.add_subplot(212)
    
    ax2.plot(saxToMatrix, color = 'g')
    plt.show()

def readData(relativePath, nbr):
        path = (os.getcwd()[:len(os.getcwd())])

        with open(path + "\\" + relativePath) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                return [float(i) for i in row]

if __name__ == '__main__':
    aantalLetters = 8
    waardesPerLetter = 15

    data1 = readData('Data2\\test7_B.csv', 23)
    data2 = readData('Data2\\test29_B.csv', 23)
     
    timeSeq1 = TimeSequence.TimeSequence(data1, aantalLetters, waardesPerLetter)
    
    timeSeq2 = TimeSequence.TimeSequence(data1, aantalLetters, waardesPerLetter)

    #timeSeq1.filter()
    #timeSeq2.filter()

    timeSeq = timeSeq1.extend(timeSeq2)

    timeSeq.filter()

    sortedMatrix = sorted(timeSeq.getMatrix())
    timeSeq.makeThresholds(sortedMatrix)
    timeSeq.makeSaxString(sortedMatrix)

    thresholdSol = ThresholdSolution.ThresholdSolution(timeSeq, {"Left" : "c", "Right" : "f"}, 14)
    thresholdSol.processTimeSequence()

    plot_data_saxString(timeSeq,aantalLetters,waardesPerLetter)
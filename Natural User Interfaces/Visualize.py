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
import PatternSolution
import Sax
import SaxWord
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
    ax1 = fig.add_subplot(111)
    #lines = ax1.plot(timeSeq.getMatrix())
    ax1.tick_params(axis='both', labelsize=36)
    #plt.setp(lines, linewidth=3)
    plt.xlim(0, 4900)
    plt.ylim(-40000,40000)
    lines2 = ax1.plot(saxToMatrix, color = '#009900')
    plt.setp(lines2, linewidth=2)
    #for threshold in timeSeq.getThresholds():
    #ax1.add_line(plt.axhline(y=timeSeq.getThresholds()[1], color = 'r'))
    #ax1.add_line(plt.axhline(y=timeSeq.getThresholds()[7], color = 'r'))
    #ax1.add_line(plt.axhline(y = -26200, xmin = 330/4900, xmax = 460/4900, linewidth = 3, color = 'b'))
    #ax1.add_line(plt.axhline(y = -26200, xmin = 1514/4900, xmax = 1710/4900, linewidth = 3, color = 'b'))
    #ax1.add_line(plt.axhline(y = -26200, xmin = 3160/4900, xmax = 3433/4900, linewidth = 3, color = 'b'))
    #ax1.add_line(plt.axhline(y = 22300, xmin = 888/4900, xmax = 1069/4900, linewidth = 3, color = 'b'))
    #ax1.add_line(plt.axhline(y = 22300, xmin = 2249/4900, xmax = 2563/4900, linewidth = 3, color = 'b'))
    #ax1.add_line(plt.axhline(y = 22300, xmin = 3960/4900, xmax = 4063/4900, linewidth = 3, color = 'b'))
    #ax1.plot(range(868,1030),saxToMatrix[868:1030], linewidth = 3, color = 'r')
    #ax1.plot(range(2248,2374),saxToMatrix[2248:2374], linewidth = 3, color = 'b')
    #ax1.plot(range(3944,4050),saxToMatrix[3944:4050], linewidth = 3, color = 'b')

    #ax1.plot(range(285,400),saxToMatrix[285:400], linewidth = 3, color = 'r')
    #ax1.plot(range(1486,1600),saxToMatrix[1486:1600], linewidth = 3, color = 'b')
    #ax1.plot(range(3136,3300),saxToMatrix[3136:3300], linewidth = 3, color = 'b')

    #ax2 = fig.add_subplot(212)
    plt.xlim(0, 4900)
    plt.ylim(-40000,40000)
    #ax2.plot(saxToMatrix, color = 'g')
    plt.show()

def readData(relativePath, nbr):
        path = (os.getcwd()[:len(os.getcwd())])

        with open(path + "\\" + relativePath) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                return [float(i) for i in row]

if __name__ == '__main__':
    maxMatchingDistance = 25
    alphabetSize = 8
    valuesPerLetter = 15

    #data1 = readData('PosterData\\test006_B.csv', 23)
    #data2 = readData('PosterData\\test006_B.csv', 23)
    path = 'Data2\\test20_B.csv'
    matrix = readData(path, 23)[:4900]
    matrix2 = np.zeros(4900)

    for i in range(len(matrix)):
        matrix2[i] = matrix[i] - 8*i
     
    timeSeq = TimeSequence.TimeSequence(matrix2, alphabetSize, valuesPerLetter)
    
    #timeSeq2 = TimeSequence.TimeSequence(data2, aantalLetters, waardesPerLetter)

    timeSeq.filter()
    #timeSeq2.filter()

    #timeSeq = timeSeq1.extend(timeSeq2)

    #timeSeq.filter()

    sortedMatrix = sorted(timeSeq.getMatrix())
    timeSeq.makeThresholds(sortedMatrix)
    timeSeq.makeSaxString(sortedMatrix)
    thresholds = timeSeq.getThresholds()

    #thresholdSol = ThresholdSolution.ThresholdSolution({"Left" : "c", "Right" : "f"}, 14)
    #thresholdSol.processTimeSequenceCalibration(timeSeq)

    saxWord1 = SaxWord.SaxWord(timeSeq.getMatrix()[265:865], alphabetSize, valuesPerLetter, thresholds)
    saxWord2 = SaxWord.SaxWord(timeSeq.getMatrix()[2765:3365], alphabetSize, valuesPerLetter, thresholds)
    calibrationDict = {"Left": [saxWord1, saxWord2]}

    patternSol = PatternSolution.PatternSolution(maxMatchingDistance, alphabetSize, valuesPerLetter, thresholds)
    patternSol.processTimeSequenceCalibration(calibrationDict)

    plot_data_saxString(timeSeq,alphabetSize,valuesPerLetter)
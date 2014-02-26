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
    
def plot_data_saxString(eog,aantal):
    eog.makeSaxString(aantal)
    saxToMatrix = []
    lst = "abcdefghijklmnopqrstuvwxyz"
    for letter in eog.getSaxString():
        for letterIndex in range(aantal):
            if letter == lst[letterIndex]:
                waarde = (eog.getThresholds()[letterIndex] + eog.getThresholds()[letterIndex+1]) / 2
                for i in range(aantal):
                    saxToMatrix.append(waarde)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(eog.getMatrix())
    ax1.plot(saxToMatrix, color = 'g')
    
    ax2 = fig.add_subplot(212)
    
    ax2.plot(saxToMatrix, color = 'g')
    plt.show()

eog1 = Eog.Eog('Data2\\test26_B.csv',23)
eog2 = Eog.Eog('Data2\\test27_B.csv',23)

#eog1.filter()
#eog2.filter()


eog1.append(eog2)



aantal = 20

plot_data_saxString(eog1,aantal)
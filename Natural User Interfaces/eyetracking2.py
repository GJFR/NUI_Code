#!/usr/bin/env python
# encoding: utf-8
#
# On mac, follow these steps:
# - Install serial to usb driver for the FTDI interface:
#   http://pbxbook.com/other/mac-tty.html
# - Set serial to '/dev/cu.usbserial-AD024JA7' (or ...A5)
#
# On windows, follow these steps:
# - Set serial to 'COM4'
#
# Background:
# - http://stackoverflow.com/questions/8265938/live-plotting-using-pyserial-and-matplotlib
#
# Copyright 2013, Wannes Meert, KU Leuven
#

import io
import serial
import threading
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.signal import filtfilt, butter
from time import sleep
from struct import *

#port = '/dev/cu.usbserial-AD024JA5'
port = 'COM3'
baud = 115200


#serial_port.setDTR()

eog1 = np.zeros(1000)
eog2 = np.zeros(1000)

eog1_filt = np.zeros(1000)
eog2_filt = np.zeros(1000)

def handle_data(data):
    print(data)

def align_data(ser):
    align=0

    while align!=3:
      aByte = Struct('B')
      byteData = ser.read(1)
      byteVal = aByte.unpack(byteData)

#      print("byte={}".format(byteVal))

      if align>0:
        if byteVal==(0,):
          align+=1
        else:
          align=0

      if align==0 and byteVal==(192,):
        align=1

#      print("align={}".format(align))

    ser.read(80)


def read_from_port(runQueue, runLock):
    global connected
    global eog1
    global eog2

    #ser.flushInput()
    #ser.flushOutput()

    ser = serial.Serial(port,
                            baud,
                            timeout=None, # Wait for requested nb of bytes
                            #timeout=1, # Wait for 1 sec for requested nb of bytes
                            bytesize=serial.EIGHTBITS)
    connected = False
    while not connected:
        #serin = ser.read()
        connected = True

        align_data(ser)

        ss = Struct('B'*3)
        s1 = Struct('i'*10)
        s2 = Struct('i'*10)
        print("s1 size = {}, s2 size = {}".format(s1.size, s2.size))

        #eog1_full = np.zeros(30000)
        #eog2_full = np.zeros(30000)

        #while True:
        for t in range(999999):
          print("Loop: {}".format(t))

          eog1[0:990] = eog1[10:1000]
          eog2[0:990] = eog2[10:1000]
          datas = ser.read(3)
          #print("datas={}".format(datas))
          if len(datas) > 0:
            #status = np.frombuffer(datas, count=3, dtype=np.uint8) # 3*1 byte
            status = ss.unpack(datas)
            # Should be (127,0,0)
            #print("Status: {}".format(status))

          # Read 10 objects from each
          data1 = ser.read(40)
          #print("data1={}".format(data1))
          data2 = ser.read(40)
          #print("data2={}".format(data2))
          if len(data1) > 0 and len(data2) > 0:
            if len(data1) != 40 or len(data2) != 40:
              print("Data is not of length 40, ignoring data")
              continue
            try:
              #val1 = np.frombuffer(data1, count=10, dtype=np.int32) # 10*4 byte
              val1 = s1.unpack(data1)
              #print("val1:")
              #print(val1)

              #val2 = np.frombuffer(data2, count=10, dtype=np.int32) # 10*4 byte
              val2 = s2.unpack(data2)
              #print("val2:")
              #print(val2)

              eog1[990:1000] = val1
              eog2[990:1000] = val2
              bool = runLock.acquire(False)
              if (bool):
                runQueue.put(val2)
            except ValueError as err:
              print("ValueError: {}".format(err))
              print(data1)
              print(data2)
          else:
            print("Data was length {} and {}, ignoring data".format(len(data1), len(data2)))

          sleep(0.0001)

    print("Closing serial port ...")
    ser.close()
    print("... closed")

def read_from_port2(runQueue, amount):
    global connected
    global eog1
    global eog2

    #ser.flushInput()
    #ser.flushOutput()

    ser = serial.Serial(port,
                            baud,
                            timeout=None, # Wait for requested nb of bytes
                            #timeout=1, # Wait for 1 sec for requested nb of bytes
                            bytesize=serial.EIGHTBITS)
    connected = False
    while not connected:
        #serin = ser.read()
        connected = True

        align_data(ser)

        ss = Struct('B'*3)
        s1 = Struct('i'*10)
        s2 = Struct('i'*10)
        print("s1 size = {}, s2 size = {}".format(s1.size, s2.size))

        #eog1_full = np.zeros(30000)
        #eog2_full = np.zeros(30000)

        #while True:
        for t in range(amount):
          print("Loop: {}".format(t))

          eog1[0:990] = eog1[10:1000]
          eog2[0:990] = eog2[10:1000]
          datas = ser.read(3)
          print("datas={}".format(datas))
          if len(datas) > 0:
            #status = np.frombuffer(datas, count=3, dtype=np.uint8) # 3*1 byte
            status = ss.unpack(datas)
            # Should be (127,0,0)
            print("Status: {}".format(status))

          # Read 10 objects from each
          data1 = ser.read(40)
          print("data1={}".format(data1))
          data2 = ser.read(40)
          print("data2={}".format(data2))
          if len(data1) > 0 and len(data2) > 0:
            if len(data1) != 40 or len(data2) != 40:
              print("Data is not of length 40, ignoring data")
              continue
            try:
              #val1 = np.frombuffer(data1, count=10, dtype=np.int32) # 10*4 byte
              val1 = s1.unpack(data1)
              print("val1:")
              print(val1)

              #val2 = np.frombuffer(data2, count=10, dtype=np.int32) # 10*4 byte
              val2 = s2.unpack(data2)
              print("val2:")
              print(val2)

              eog1[990:1000] = val1
              eog2[990:1000] = val2
              runQueue.extend(val2)
            except ValueError as err:
              print("ValueError: {}".format(err))
              print(data1)
              print(data2)
          else:
            print("Data was length {} and {}, ignoring data".format(len(data1), len(data2)))

          sleep(0.0001)

    print("Closing serial port ...")
    ser.close()
    print("... closed")

def plot_data():

  print("Init plotting")
  #b, a = butter(2, 0.0001, 'high')
  b, a = butter(2, 0.5, 'high')

  fig = plt.figure()
  ax1 = fig.add_subplot(211)
  ax2 = fig.add_subplot(212)
  line1, = ax1.plot(eog1)
  line2, = ax2.plot(eog2)
  fig.show()

  print("Start plotting")

  #while True:
  for t in range(5*12):

    print("Filtering")
    eog1_filt = filtfilt(b, a, eog1)
    eog2_filt = filtfilt(b, a, eog2)

    print("Plotting")
    line1.set_ydata(eog1_filt)
    ax1.set_ylim((min(eog1_filt), max(eog1_filt)))
    line2.set_ydata(eog2_filt)
    ax2.set_ylim((min(eog2_filt), max(eog2_filt)))
    fig.canvas.draw()
    fig.show()

    sleep(.5)

  print("Plotting ended")



global runQueue
global runLock
global accessLock
global amount

def run(inputQueue, queueLock, queueAccessLock):
    runQueue = inputQueue
    runLock = queueLock
    accessLock = queueAccessLock
    thread = threading.Thread(target=read_from_port, args=(runQueue,runLock))
    thread.start()
    plot_data()


def run2(inputQueue, amountOfValues):
    
    runQueue = inputQueue
    amount = amountOfValues
    read_from_port2(runQueue, amount)
    return runQueue

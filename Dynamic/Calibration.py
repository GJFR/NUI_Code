'''
Created on 9-dec.-2013

@author: Kevin & Gertjan
'''

import IOFunctions
import threading

if __name__ == '__main__':
    pass

def calibrate(directions):
    groups = []
    thread = threading.Thread(target=IOFunctions.IOCalibration(), args=groups)
    thread.start()
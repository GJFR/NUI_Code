'''
Created on 30-apr.-2014

@author: Kevin
'''
import socket
import atexit


HOST = 'localhost'
PORT = 42001

def saveData(socket, path):
    
    while True:
        file = open(path, 'a')
        
        for i in range(100):
            file.write(str(readData(socket))+",")    
        file.close()
        #print("closed")
    
def readData(socket):
    while True:
        size = int.from_bytes(socket.recv(4), byteorder = "big")
            
        data = str(socket.recv(size), encoding = "UTF-8")
        if ("eogDongle" in data):
            value = int(data[28:])
        else:
            continue
        
        
        channel = int(data[26:27])
        waarde = value
    
        if channel == 1:
            return waarde

def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    saveData(s,'Data.csv')

if __name__ == '__main__':
    run()
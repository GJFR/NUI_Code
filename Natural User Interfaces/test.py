'''
Created on 29-apr.-2014

@author: Kevin
'''

import socket

HOST = 'localhost'
PORT = 42001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def sendCMD(cmd):
    n = len(cmd)
    a = []
    a.append((n >> 24) & 0xFF)
    a.append((n >> 16) & 0xFF)
    a.append((n >> 8) & 0xFF)
    a.append(n & 0xFF)
    b = ''
    for i in list(range(len(a))):
        b  += str(a[i])
    s.send(bytes(b+cmd,'UTF-8'))

while True:
    data = s.recv(50)[30:31]
    print(int(str(data, encoding = "UTF-8")))
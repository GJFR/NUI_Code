'''
Created on 2 dec. 2013

@author: Kevin
'''

import unittest
import Sax

class TestSax(unittest.TestCase):
    
    def setUp(self):
        self.timeSeq = Sax.TimeSequence(range(10),[0,5,9],2,4,3,4,2,1)

    def testConstructor(self):
        pass

#####################################################################
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    

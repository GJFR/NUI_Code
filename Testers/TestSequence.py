'''
Created on 2-dec.-2013

@author: Gertjan
'''
import unittest
import math
import Sequence


class TestSequence(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.data = range(200)
        '''Original sequences'''
        self.start = 49
        self.length = 100
        self.seq = Sequence.Sequence(self.data, self.start, self.length)
        self.start2 = 50
        self.seq2 = Sequence.Sequence(self.data, self.start2, self.length)
        self.length3 = 2
        self.length4 = 4
        self.seq3 = Sequence.Sequence(self.data, self.start2, self.length3)
        self.seq4 = Sequence.Sequence(self.data, self.start2, self.length4)
        '''Normalized sequences'''
        self.nSeq = self.seq.getNormalized()
        self.nSeq2 = self.seq2.getNormalized()
        self.nSeq3 = self.seq3.getNormalized()
        self.nSeq4 = self.seq4.getNormalized()
        '''Scaled sequences'''
        self.sSeq4 = Sequence.ScaledSequence(self.data, self.seq4, 8)
    
    def testConstructor(self):
        self.assertEqual(self.seq.getStart(), self.start)
        self.assertEqual(self.seq.getLength(), self.length)
        self.assertEqual(self.seq.getPoint(62), self.data[49 + 62])
        with self.assertRaises(IndexError):
                self.seq.getPoint(103)
        self.assertEqual(self.seq.getAllPoints(), self.data[49:149])
        
    def testGetDistance(self):
        self.assertEqual(self.seq.getDistance(self.seq2), 1)
        self.assertEqual(self.nSeq.getDistance(self.nSeq2), 1)
    
    def testNormalized(self):
        self.assertEqual(self.nSeq2.getOriginal(), self.seq2)
        with self.assertRaises(IndexError):
            self.nSeq2.getPoint(103)
        self.assertEqual(self.nSeq3.getAllPoints(), [-1,1])
        self.assertEqual(self.nSeq4.getAllPoints(), [-1,-1/3,1/3,1])
    
    def testCompare(self):
        self.assertEqual(self.nSeq.compare(self.nSeq), 0)
        self.assertEqual(self.nSeq.compare(self.nSeq2), 0)
        self.assertAlmostEqual(self.nSeq3.compare(self.nSeq4), math.sqrt(8/9))
        
    def testGetLetter(self):
        self.assertEqual(self.seq.getLetter(.9, 3), 'c')
        self.assertEqual(self.seq.getLetter(0, 3), 'b')
        self.assertEqual(self.seq.getLetter(-.6, 3), 'a')
        
    def testGetWord(self):
        self.assertEqual(self.nSeq4.getWord(4, 3), 'abbc')
        self.assertEqual(self.nSeq4.getWord(4, 6), 'acdf')
        self.assertEqual(self.nSeq4.getWord(2, 3), 'ac')
        with self.assertRaises(AttributeError):
            self.seq.getWord(110, 20)
        
    def testScaled(self):
        self.assertEqual(self.sSeq4.getOriginal(), self.seq4)
        with self.assertRaises(IndexError):
            self.nSeq4.getPoint(103)
        self.assertEqual(self.sSeq4.getAllPoints(), [50, 50, 51, 51, 52, 52, 53, 53])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
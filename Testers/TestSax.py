'''
Created on 2 dec. 2013

@author: Kevin
'''

import unittest
import Sax
import Sequence
import scipy
import itertools
import math

class TestSax(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.data = range(25)
        self.verdeelPunten = [0,10,20]
        self.minSeqLengte = 4
        self.maxSeqLengte = 6
        self.woordLengte = 2
        self.alfabetGrootte = 4
        self.collisionThreshold = 2
        self.r = 1
        self.timeSeq = Sax.TimeSequence(self.data, self.verdeelPunten, self.minSeqLengte, self.maxSeqLengte, self.woordLengte, self.alfabetGrootte, self.collisionThreshold, self.r)
        
        self.sArray = ["abcd", "bbde", "bcda", "bdee", "abed", "ddac", "cccc", "dcba", "abab", "bcdc", "abad", "ebee", "bbbb", "bbbd", "ccaa"]
        self.mask = [0,2]
        self.dictie = {"bd" : [0,4,10,13], "be" : [1,11], "ca" : [2,7,14], "de" : [3],"dc" : [5] ,"cc" : [6,9], "bb" : [8,12]}
        
        
        

    def testConstructor(self):
        self.assertEqual(self.timeSeq.verdeelPunten, self.verdeelPunten, "Constructor:verdeelPunten")
        self.assertEqual(self.timeSeq.minSeqLengte, self.minSeqLengte, "Constructor:minSeqLengte")
        self.assertEqual(self.timeSeq.maxSeqLengte, self.maxSeqLengte, "Constructor:maxSeqLengte")
        self.assertEqual(self.timeSeq.woordLengte, self.woordLengte, "Constructor:woordLengte")
        self.assertEqual(self.timeSeq.alfabetGrootte, self.alfabetGrootte, "Constructor:alfabetGrootte")
        self.assertEqual(self.timeSeq.collisionThreshold, self.collisionThreshold, "Constructor:collisionThreshold")
        self.assertEqual(self.timeSeq.r, self.r, "Constructor:r")
        self.assertEqual(len(self.timeSeq.sequenceList), 352, "Constructor:sequenceList:len")
        
        for seq in self.timeSeq.sequenceList:
            self.assertIsInstance(seq, Sequence.NormSequence, "Constructor:sequenceList:class")
        
        
    
#     def testGetSaxArray(self):
#         pass
#         self.sArray = self.timeSeq.getSaxArray()
#         
#         self.assertEqual(self.sArray[0], "acd", "saxArray:0")
#         self.assertEqual(self.sArray[1], "acd", "saxArray:1")
#         self.assertEqual(self.sArray[2], "acd", "saxArray:2")
#         self.assertEqual(self.sArray[3], "acd ", "saxArray:3")
#         self.assertEqual(self.sArray[4], "acd ", "saxArray:4")
#         self.assertEqual(self.sArray[5], "acd ", "saxArray:5")
#         self.assertEqual(self.sArray[6], "acd ", "saxArray:6")
#         self.assertEqual(self.sArray[7], "acd ", "saxArray:7")
#         self.assertEqual(self.sArray[8], "acd" , "saxArray:8")
#         self.assertEqual(self.sArray[9], "acd", "saxArray:9")
#         self.assertEqual(self.sArray[10], "acd", "saxArray:10")
#         self.assertEqual(self.sArray[11], "acd", "saxArray:11")
#         self.assertEqual(self.sArray[12], "acd ", "saxArray:12")
#         self.assertEqual(self.sArray[13], "acd ", "saxArray:13")
#         self.assertEqual(self.sArray[14], "acd ", "saxArray:14")
    
    def testGetCollisionMatrix(self):
        pass
    
    def testMask(self):
        sArray2 = ["abcd", "bbde", "bcda", "bdee", "abed", "ddac", "cccc", "dabc", "abab", "bcdb"]
        self.mask = [0,2]
        
        sArray2 = self.timeSeq.mask(sArray2, self.mask)
        
        self.assertEqual(sArray2[0], "bd", "self.mask:0")
        self.assertEqual(sArray2[1], "be", "self.mask:1")
        self.assertEqual(sArray2[2], "ca", "self.mask:2")
        self.assertEqual(sArray2[3], "de", "self.mask:3")
        self.assertEqual(sArray2[4], "bd", "self.mask:4")
        self.assertEqual(sArray2[5], "dc", "self.mask:5")
        self.assertEqual(sArray2[6], "cc", "self.mask:6")
        self.assertEqual(sArray2[7], "ac", "self.mask:7")
        self.assertEqual(sArray2[8], "bb", "self.mask:8")
        self.assertEqual(sArray2[9], "cb", "self.mask:9")
    
    def testFHash(self):

        
        hashy = self.timeSeq.fHash(self.sArray, self.mask)
        for sax in hashy:
            self.assertEqual(hashy[sax], self.dictie[sax], "fhash" + sax)
        
    def testCheckBuckets(self):
        cMatrix = scipy.sparse.lil_matrix((len(self.sArray),len(self.sArray)))
        hashy = self.timeSeq.fHash(self.sArray, self.mask)
        self.timeSeq.checkBuckets(hashy, cMatrix)
        cooMatrix = cMatrix.tocoo()
        for i,j,v in itertools.zip_longest(cooMatrix.row, cooMatrix.col, cooMatrix.data):
            aantal = 0
            for key in self.dictie:
                if i in self.dictie[key] and j in self.dictie[key]:
                    aantal += 1
            self.assertEqual(v, aantal, "CheckBuckets: " + str(i) + " : " + str(j))
        
    def testTest(self):
        for i in range(9):
            for j in range(i+1,9):
                self.assertFalse(self.timeSeq.test(i, j), "testFalse:" + str(i) + " : " + str(j))
        for i in range(9,15):
            for j in range(i+1,15):
                self.assertFalse(self.timeSeq.test(i, j), "testFalse:" + str(i) + " : " + str(j))
        for i in range(9):
            for j in range(9,15):
                self.assertTrue(self.timeSeq.test(i, j),  "testTrue:" + str(i) + " : " + str(j))
        
    def testLikelyPairs(self):
        cMatrix = scipy.sparse.lil_matrix((len(self.sArray),len(self.sArray)))
        self.timeSeq.checkBuckets(self.timeSeq.fHash(self.sArray, [0,2]), cMatrix)
        self.timeSeq.checkBuckets(self.timeSeq.fHash(self.sArray, [1,3]), cMatrix)
        self.timeSeq.checkBuckets(self.timeSeq.fHash(self.sArray, [0,2]), cMatrix)

        Tlist = self.timeSeq.getLikelyPairs(cMatrix)
        print (Tlist)
        for i,j in Tlist:
            print("a")
            self.assertGreaterEqual(cMatrix[self.timeSeq.sequenceList.index(i), self.timeSeq.sequenceList.index(j)], 2, "LikelyPairs:" + str(i)+" : "+ str(j))


           
#####################################################################


    def testGetMotifs(self):
        data = range(20)
        data.extend([20])
        data.extend(range(21,40))
        timeSeq = Sax.TimeSequence(data, self.verdeelPunten, self.minSeqLengte, self.maxSeqLengte, self.woordLengte, self.alfabetGrootte, self.collisionThreshold, self.r)
        timeSeq.getMotifs(),
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    

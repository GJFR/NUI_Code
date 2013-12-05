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
        
        self.sArray = self.timeSeq.getSaxArray()
        
        a = set(range(36)) - set(range(7,13)) - set(range(25,31))
        b = set(range(31)) - set(range(7)) - set(range(13,25))
        self.dictie = {"c": a, "d" : b}
        

    def testConstructor(self):
        self.assertEqual(self.timeSeq.verdeelPunten, self.verdeelPunten, "Constructor:verdeelPunten")
        self.assertEqual(self.timeSeq.minSeqLengte, self.minSeqLengte, "Constructor:minSeqLengte")
        self.assertEqual(self.timeSeq.maxSeqLengte, self.maxSeqLengte, "Constructor:maxSeqLengte")
        self.assertEqual(self.timeSeq.woordLengte, self.woordLengte, "Constructor:woordLengte")
        self.assertEqual(self.timeSeq.alfabetGrootte, self.alfabetGrootte, "Constructor:alfabetGrootte")
        self.assertEqual(self.timeSeq.collisionThreshold, self.collisionThreshold, "Constructor:collisionThreshold")
        self.assertEqual(self.timeSeq.r, self.r, "Constructor:r")
        self.assertEqual(len(self.timeSeq.sequenceList), 36, "Constructor:sequenceList:len")
        
        for seq in self.timeSeq.sequenceList:
            self.assertIsInstance(seq, Sequence.NormSequence, "Constructor:sequenceList:class")
        

        for i in range(7):
            self.assertEqual(self.timeSeq.sequenceList[i].getStart(),i)
            self.assertEqual(self.timeSeq.sequenceList[i].getLength(),4)
        for i in range(7,13):
            self.assertEqual(self.timeSeq.sequenceList[i].getStart(),i-7)
            self.assertEqual(self.timeSeq.sequenceList[i].getLength(),5)
        for i in range(13,18):
            self.assertEqual(self.timeSeq.sequenceList[i].getStart(),i-13)
            self.assertEqual(self.timeSeq.sequenceList[i].getLength(),6)
        for i in range(18,25):
            self.assertEqual(self.timeSeq.sequenceList[i].getStart(),i-8)
            self.assertEqual(self.timeSeq.sequenceList[i].getLength(),4)
        for i in range(25,31):
            self.assertEqual(self.timeSeq.sequenceList[i].getStart(),i-15)
            self.assertEqual(self.timeSeq.sequenceList[i].getLength(),5)
        for i in range(31,36):
            self.assertEqual(self.timeSeq.sequenceList[i].getStart(),i-21)
            self.assertEqual(self.timeSeq.sequenceList[i].getLength(),6)
        
        for seq in self.timeSeq.sequenceList:
            self.assertEqual(seq.getLength(), len(seq.getAllPoints()), "verkeerde sequences")
    
    def testGetSaxArray(self):
        
        for i in range(7):
            self.assertEqual(self.sArray[i], "bc", "saxArray:" + str(i))
        for i in range(7,13):
            self.assertEqual(self.sArray[i], "bd" , "saxArray:" + str(i))
        for i in range(13,25):
            self.assertEqual(self.sArray[i], "bc", "saxArray:" + str(i))
        for i in range(25,31):
            self.assertEqual(self.sArray[i], "bd", "saxArray:" + str(i))
        for i in range(31,36):
            self.assertEqual(self.sArray[i], "bc", "saxArray:" + str(i))
    
    def testGetCollisionMatrix(self):
        masks = [[0],[1]]
        cMatrix1 = self.timeSeq.getCollisionMatrix(masks)
        cooMatrix = cMatrix1.tocoo()
        print(cooMatrix)
        cMatrix = scipy.sparse.lil_matrix((36,36))

        for i in range(0,18):
            for j in range(18,36):
                cMatrix[i,j] += 2
        for i in range(7):
            for j in range(25,31):
                cMatrix[i,j] -= 1
        for i in range(13,18):
            for j in range(25,31):
                cMatrix[i,j] -= 1
        for i in range(7,13):
            for j in range(18,25):
                cMatrix[i,j] -= 1
            for j in range(31,36):
                cMatrix[i,j] -= 1
        

        for i,j,v in itertools.zip_longest(cooMatrix.row, cooMatrix.col, cooMatrix.data):
            self.assertEqual(v, cMatrix[i,j], str(i) + "," + str(j) + ":" + str(v))
            
            
    def testGetMasks(self):
        masks = self.timeSeq.getMasks()
        
        self.assertEqual(len(masks), self.woordLengte, "getMasks:length")
        
        for mask in masks:
            mask.sort()
            self.assertGreaterEqual(len(mask), 1, "getMasks:mask:MinLength")
            self.assertLess(len(mask), self.woordLengte, "getMasks:mask:MaxLength")
            self.assertEqual(len(mask), len(set(mask)), "getMasks:mask:duplicates")
            for m in mask:
                self.assertIn(m, range(self.woordLengte), "getMasks:point:outOfRange")
        for mask1 in masks:
            for mask2 in masks:
                if mask1 != mask2:
                    with self.assertRaises(AssertionError):
                        self.assertListEqual(mask1, mask2, "getMasks:equal Masks")
    
    def testMask(self):
        sArray2 = ["ab", "bb", "bc", "bd", "ab", "dd", "cc", "da", "ab", "bc"]
        self.mask = [0]
        
        sArray2 = self.timeSeq.mask(sArray2, self.mask)
        
        self.assertEqual(sArray2[0], "b", "self.mask:0")
        self.assertEqual(sArray2[1], "b", "self.mask:1")
        self.assertEqual(sArray2[2], "c", "self.mask:2")
        self.assertEqual(sArray2[3], "d", "self.mask:3")
        self.assertEqual(sArray2[4], "b", "self.mask:4")
        self.assertEqual(sArray2[5], "d", "self.mask:5")
        self.assertEqual(sArray2[6], "c", "self.mask:6")
        self.assertEqual(sArray2[7], "a", "self.mask:7")
        self.assertEqual(sArray2[8], "b", "self.mask:8")
        self.assertEqual(sArray2[9], "c", "self.mask:9")
        
        sArray2 = ["ab", "bb", "bc", "bd", "ab", "dd", "cc", "da", "ab", "bc"]
        self.mask = [1]
        
        sArray2 = self.timeSeq.mask(sArray2, self.mask)
        
        self.assertEqual(sArray2[0], "a", "self.mask:0")
        self.assertEqual(sArray2[1], "b", "self.mask:1")
        self.assertEqual(sArray2[2], "b", "self.mask:2")
        self.assertEqual(sArray2[3], "b", "self.mask:3")
        self.assertEqual(sArray2[4], "a", "self.mask:4")
        self.assertEqual(sArray2[5], "d", "self.mask:5")
        self.assertEqual(sArray2[6], "c", "self.mask:6")
        self.assertEqual(sArray2[7], "d", "self.mask:7")
        self.assertEqual(sArray2[8], "a", "self.mask:8")
        self.assertEqual(sArray2[9], "b", "self.mask:9")
    
    def testFHash(self):

        
        hashy = self.timeSeq.fHash(self.sArray, [0])
        for sax in hashy:
            self.assertEqual(hashy[sax], list(self.dictie[sax]), "fhash" + sax)
        
    def testCheckBuckets(self):
        cMatrix = scipy.sparse.lil_matrix((len(self.sArray),len(self.sArray)))
        hashy = self.timeSeq.fHash(self.sArray, [0])
        self.timeSeq.checkBuckets(hashy, cMatrix)
        cooMatrix = cMatrix.tocoo()

        for i,j,v in itertools.zip_longest(cooMatrix.row, cooMatrix.col, cooMatrix.data):
            aantal = 0
            for key in self.dictie:
                if i in self.dictie[key] and j in self.dictie[key]:
                    aantal += 1
            self.assertEqual(v, aantal, "CheckBuckets: " + str(i) + " : " + str(j))
        
    def testTest(self):
        for i in range(18):
            for j in range(i+1,18):
                self.assertFalse(self.timeSeq.test(i, j), "testFalse:" + str(i) + " : " + str(j))
        for i in range(18,36):
            for j in range(i+1,36):
                self.assertFalse(self.timeSeq.test(i, j), "testFalse:" + str(i) + " : " + str(j))
        for i in range(18):
            for j in range(18,36):
                self.assertTrue(self.timeSeq.test(i, j),  "testTrue:" + str(i) + " : " + str(j))
        
    def testLikelyPairs(self):
        cMatrix = scipy.sparse.lil_matrix((len(self.sArray),len(self.sArray)))
        self.timeSeq.checkBuckets(self.timeSeq.fHash(self.sArray, [0,2]), cMatrix)
        self.timeSeq.checkBuckets(self.timeSeq.fHash(self.sArray, [1,3]), cMatrix)
        self.timeSeq.checkBuckets(self.timeSeq.fHash(self.sArray, [0,2]), cMatrix)

        Tlist = self.timeSeq.getLikelyPairs(cMatrix)
        self.assertGreater(len(Tlist), 0)
        for i,j in Tlist:
            self.assertGreaterEqual(cMatrix[self.timeSeq.sequenceList.index(i), self.timeSeq.sequenceList.index(j)], 2, "LikelyPairs:" + str(i)+" : "+ str(j))


           
#####################################################################


    def testGetMotifs(self):
        data = list(range(30))
        data.extend([30] * 10)
        '''7 motieven: 0, 1, 2, 3, 4, 5, 6'''
        data.extend(range(31,60))
        '''6 motieven: 30, 31, 32, 33, 34, 35'''
        verdeelPunten1 = [0,35,70]
        verdeelPunten2 = [0,35,69]
        with self.assertRaises(AttributeError):
            timeSeq = Sax.TimeSequence(data, verdeelPunten1, 25, 25, 5, 5, 2, self.r)
        timeSeq = Sax.TimeSequence(data, verdeelPunten2, 25, 25, 5, 5, 1, 0)
        masks = [[0,1],[1,2],[2,3],[3,4],[0,1,2],[1,2,3],[2,3,4]]
        cMatrix = timeSeq.getCollisionMatrix(masks)
        motifs = timeSeq.getMotifs(cMatrix)
        self.assertEqual(len(motifs), 13)
        '''Totaal: 7 + 6 = 13 motieven'''
    
    def testRemoveCloseMatches(self):
        data = list(range(30))
        data.extend([30] * 10)
        '''7 motieven: 0, 1, 2, 3, 4, 5, 6'''
        data.extend(range(31,60))
        '''6 motieven: 30, 31, 32, 33, 34, 35'''
        verdeelPunten1 = [0,35,70]
        verdeelPunten2 = [0,35,69]
        with self.assertRaises(AttributeError):
            timeSeq = Sax.TimeSequence(data, verdeelPunten1, 25, 25, 5, 5, 2, self.r)
        timeSeq = Sax.TimeSequence(data, verdeelPunten2, 25, 25, 5, 5, 1, 0)
        masks = [[0,1],[1,2],[2,3],[3,4],[0,1,2],[1,2,3],[2,3,4]]
        cMatrix = timeSeq.getCollisionMatrix(masks)
        motifs = timeSeq.getMotifs(cMatrix)
        self.assertEqual(len(motifs), 13)
        '''Totaal: 7 + 6 = 13 motieven'''
        timeSeq.removeCloseMatches(motifs)
        self.assertEqual(len(motifs), 13)
        for motif in motifs:
            self.assertEqual(len(motifs[motif]),1)

    def testRemoveTrivialMotifs(self):
        data = list(range(30))
        data.extend([30] * 10)
        '''7 motieven: 0, 1, 2, 3, 4, 5, 6'''
        data.extend(range(31,60))
        '''6 motieven: 30, 31, 32, 33, 34, 35'''
        verdeelPunten1 = [0,35,70]
        verdeelPunten2 = [0,35,69]
        with self.assertRaises(AttributeError):
            timeSeq = Sax.TimeSequence(data, verdeelPunten1, 25, 25, 5, 5, 2, self.r)
        timeSeq = Sax.TimeSequence(data, verdeelPunten2, 25, 25, 5, 5, 1, 0)
        masks = [[0,1],[1,2],[2,3],[3,4],[0,1,2],[1,2,3],[2,3,4]]
        cMatrix = timeSeq.getCollisionMatrix(masks)
        motifs = timeSeq.getMotifs(cMatrix)
        self.assertEqual(len(motifs), 13)
        '''Totaal: 7 + 6 = 13 motieven'''
        timeSeq.


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    

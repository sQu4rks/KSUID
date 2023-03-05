import datetime
import unittest
import time

from ksuid import ksuid

from ksuid.utils import sortKSUID

DELAY_INTERVAL_IN_SEC = 2

class KSUIDTests(unittest.TestCase):
    def setUp(self):
        self.ksList = []
        for i in range(1000):
            self.ksList.append(ksuid())

        self.ksuid1 = ksuid()
        time.sleep(DELAY_INTERVAL_IN_SEC) # Sleep to ensure that the timestamp differs
        self.ksuid2 = ksuid()

    def testTimeStamp(self):
        self.assertTrue(self.ksuid1.getTimestamp() <= self.ksuid2.getTimestamp())
        self.assertTrue(datetime.datetime.now().day == self.ksuid1.getDatetime().day)

    def testSort(self):
        self.assertTrue(len(self.ksList) > 0)
        ksList = sortKSUID(self.ksList)

        for index in range(len(ksList) - 1):
            self.assertTrue(ksList[index].getTimestamp() >= ksList[index + 1].getTimestamp())

    def testStringFunction(self):
        for val in self.ksList:
            self.assertTrue(str(val) == str(val))

    def testDifferentUIDs(self):
        for val, index in enumerate(self.ksList):
            for val2, index2 in enumerate(self.ksList):
                if index == index2:
                    continue
                self.assertTrue(str(val2) != str(val))

    def testLTOperator(self):
        self.assertTrue(self.ksuid1 < self.ksuid2)

    def testSortedOperation(self):
        l = [self.ksuid2, self.ksuid1]

        sorted_l = sorted(l)
        self.assertTrue(l[0] == self.ksuid2)
        self.assertTrue(l[1] == self.ksuid1)

        self.assertTrue(sorted_l[0] == self.ksuid1)
        self.assertTrue(sorted_l[1] == self.ksuid2)

if __name__ == "__main__":
    unittest.main()

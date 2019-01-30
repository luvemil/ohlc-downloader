import unittest

from utils.iterlist import *

class IterListTest(unittest.TestCase):
    def setUp(self):
        self.data_l = list(range(10))

    def test_unit_stride(self):
        windows = list(iterlist(self.data_l,1))
        expected_res = [ [k] for k in self.data_l ]

        self.assertSequenceEqual(windows,expected_res)

    def test_whole_stride(self):
        windows = list(iterlist(self.data_l,len(self.data_l)))
        expected_res = [ self.data_l ]

        self.assertSequenceEqual(windows,expected_res)

if __name__ == "__main__":
    unittest.main()

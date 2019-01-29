import unittest

from utils.merge_results import *
import pandas as pd

class MergeTest(unittest.TestCase):
    def test_empy_list(self):
        df = ohlcv_to_pandas([[None for x in range(6)]])

        self.assertIsInstance(df,pd.DataFrame)

if __name__ == "__main__":
    unittest.main()

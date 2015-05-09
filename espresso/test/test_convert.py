from datetime import datetime
import unittest

import pandas as pd

from espresso import convert

class ConvertTest(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame([
            {'datetime': datetime(2000,1,1,0,0), 'value': 0.0},
            {'datetime': datetime(2000,1,1,2,0), 'value': 1.0},
            {'datetime': datetime(2000,1,2,2,0), 'value': 1.0}
            ])
        self.df['datetime'] = pd.to_datetime(self.df.datetime)

    def test_aggregate_dataframe(self):
        df = convert.aggregate_dataframe(self.df)
        self.assertEqual(len(df), 2)
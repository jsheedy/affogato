import numpy as np
import pandas as pd
import unittest

from gelato import gelato


class TestGelato(unittest.TestCase):

    def setUp(self):
        self.inputData = [
            {'datetime': '2014-01-01', 'inbound': 125, 'outbound': 121},
            {'datetime': '2014-01-02', 'inbound': 263, 'outbound': 233},
            {'datetime': '2014-01-03', 'inbound': 272, 'outbound': 238},
            {'datetime': '2014-01-04', 'inbound': 230, 'outbound': 190},
            {'datetime': '2014-01-05', 'inbound': 145, 'outbound': 144},
            {'datetime': '2014-01-06', 'inbound': 306, 'outbound': 277}
            ]

        self.outputData = [
            {'fitted_inbound': 125.00000000000011,
             'residuals_inbound': -1.1368683772161603e-13,
             'residuals_outbound': -8.526512829121202e-14,
             'datetime': pd.Timestamp('2014-01-01 00:00:00'),
             'fitted_outbound': 121.00000000000009,
             'trend_inbound': 0.0,
             'trend_outbound': 0.0},
            {'fitted_inbound': 263.0000000000001,
             'residuals_inbound': -1.1368683772161603e-13,
             'residuals_outbound': -8.526512829121202e-14,
             'datetime': pd.Timestamp('2014-01-02 00:00:00'),
             'fitted_outbound': 233.00000000000009,
             'trend_inbound': 30.742514970059922,
             'trend_outbound': 27.754491017964106},
            {'fitted_inbound': 272.00000000000006,
             'residuals_inbound': -5.684341886080802e-14,
             'residuals_outbound': 0.0,
             'datetime': pd.Timestamp('2014-01-03 00:00:00'),
             'fitted_outbound': 238.0,
             'trend_inbound': 61.485029940119844,
             'trend_outbound': 55.50898203592821},
            {'fitted_inbound': 230.00000000000023,
             'residuals_inbound': -2.2737367544323206e-13,
             'residuals_outbound': -1.9895196601282805e-13,
             'datetime': pd.Timestamp('2014-01-04 00:00:00'),
             'fitted_outbound': 190.0000000000002,
             'trend_inbound': 92.22754491017977,
             'trend_outbound': 83.26347305389231},
            {'fitted_inbound': 145.00000000000023,
             'residuals_inbound': -2.2737367544323206e-13,
             'residuals_outbound': -1.9895196601282805e-13,
             'datetime': pd.Timestamp('2014-01-05 00:00:00'),
             'fitted_outbound': 144.0000000000002,
             'trend_inbound': 122.97005988023969,
             'trend_outbound': 111.01796407185643},
            {'fitted_inbound': 306.00000000000017,
             'residuals_inbound': -1.7053025658242404e-13,
             'residuals_outbound': -1.1368683772161603e-13,
             'datetime': pd.Timestamp('2014-01-06 00:00:00'),
             'fitted_outbound': 277.0000000000001,
             'trend_inbound': 153.7125748502996,
             'trend_outbound': 138.77245508982054}]

    def test_deseason(self):
        # just do a simple row count to verify functionality
        # write additional tests to verify data integrity
        actual = gelato.deseason(self.inputData)
        expected = self.outputData

        actual = pd.DataFrame(actual)
        expected = pd.DataFrame(expected)

        actual.sort(axis=1, inplace=True)
        expected.sort(axis=1, inplace=True)

        actual.sort(axis=0, inplace=True)
        expected.sort(axis=0, inplace=True)

        test = np.allclose(actual.drop('datetime', axis=1).values,
                           expected.drop('datetime', axis=1).values,
                           atol=1e-6)

        self.assertTrue(test)

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

        self.outputData = [{'datetime': pd.Timestamp('2014-01-01 00:00:00'),
                            'fitted_inbound': 125.00000000000011,
                            'fitted_outbound': 121.00000000000009,
                            'residuals_inbound': -1.1368683772161603e-13,
                            'residuals_outbound': -8.526512829121202e-14},
                           {'datetime': pd.Timestamp('2014-01-02 00:00:00'),
                            'fitted_inbound': 263.0000000000001,
                            'fitted_outbound': 233.00000000000009,
                            'residuals_inbound': -1.1368683772161603e-13,
                            'residuals_outbound': -8.526512829121202e-14},
                           {'datetime': pd.Timestamp('2014-01-03 00:00:00'),
                            'fitted_inbound': 272.00000000000006,
                            'fitted_outbound': 238.0,
                            'residuals_inbound': -5.684341886080802e-14,
                            'residuals_outbound': 0.0},
                           {'datetime': pd.Timestamp('2014-01-04 00:00:00'),
                            'fitted_inbound': 230.00000000000023,
                            'fitted_outbound': 190.0000000000002,
                            'residuals_inbound': -2.2737367544323206e-13,
                            'residuals_outbound': -1.9895196601282805e-13},
                           {'datetime': pd.Timestamp('2014-01-05 00:00:00'),
                            'fitted_inbound': 145.00000000000023,
                            'fitted_outbound': 144.0000000000002,
                            'residuals_inbound': -2.2737367544323206e-13,
                            'residuals_outbound': -1.9895196601282805e-13},
                           {'datetime': pd.Timestamp('2014-01-06 00:00:00'),
                            'fitted_inbound': 306.00000000000017,
                            'fitted_outbound': 277.0000000000001,
                            'residuals_inbound': -1.7053025658242404e-13,
                            'residuals_outbound': -1.1368683772161603e-13}]

    def test_deseason(self):
        # just do a simple row count to verify functionality
        # write additional tests to verify data integrity
        actual = gelato.deseason(self.inputData)
        expected = self.outputData

        actual = pd.DataFrame(actual)
        expected = pd.DataFrame(expected)
        self.assertTrue(actual.equals(expected))

import unittest

from gelato import gelato

class TestGelato(unittest.TestCase):

    def setUp(self):
        self.inputData = [
            {'bike_east': None,
             'bike_north': 4,
             'bike_south': 29,
             'bike_west': None,
             'datetime': '2014-02-11 12:00:00'},
            {'bike_east': None,
             'bike_north': 3,
             'bike_south': 10,
             'bike_west': None,
             'datetime': '2014-02-11 13:00:00'},
            {'bike_east': None,
             'bike_north': 5,
             'bike_south': 24,
             'bike_west': None,
             'datetime': '2014-02-11 14:00:00'},
        ]

    def test_deseasonalize(self):
        # just do a simple row count to verify functionality
        # write additional tests to verify data integrity
        actual = gelato.deseasonalize(self.inputData)
        expected = 6
        self.assertEqual(len(actual), expected)

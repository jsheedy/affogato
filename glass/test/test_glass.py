import unittest

from glass import glass

class GlassTest(unittest.TestCase):

    def test_get_counter_data_with_id(self):
        data = list(glass.get_counter_data(id=9))
        self.assertGreater(len(data), 21860)

    def test_get_aggregated_counter_data_has_unique_timestamps(self):
        data = list(glass.get_aggregated_counter_data(id=9, aggregate='daily'))
        dates = [x['datetime'] for x in data]
        dates_set = set(dates)
        self.assertEqual(len(dates), len(dates_set))

    def test_get_counter_data_without_id(self):
        data = list(glass.get_counter_data())
        self.assertGreater(len(data), 100000)

    def test_get_counters(self):
        data = list(glass.get_counters())
        self.assertGreater(len(data), 8)

    def test_get_counter(self):
        data = list(glass.get_counter(id=9))
        self.assertEqual(data[0], 9)

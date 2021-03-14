import unittest

from markov_attribution import MarkovAttribution
from pprint import pprint
from math import floor

test_data = [
  {'conversion': 1, 'value': 1000.00, 'path': 'C1 > C2 > C3'},
  {'conversion': 0, 'value': 0, 'path': 'C1'},
  {'conversion': 0, 'value': 0, 'path': 'C2 > C3'},
]

sep = ' > '


class TestAttribution(unittest.TestCase):
    def test_full_prob(self):
        marka = MarkovAttribution(test_data, sep)
        fp = marka.full_probability
        print(floor(fp*100))
        self.assertTrue(floor(fp*100) == floor(100/3))

    def test_rm_prob(self):
        marka = MarkovAttribution(test_data, sep)
        rmp = marka.cprobs['C1']['probability']
        pprint(marka.cprobs['C1'])
        print(floor(rmp*100))
        self.assertTrue(floor(rmp*100) == floor(100/6))

    def test_rm_effect(self):
        marka = MarkovAttribution(test_data, sep)
        rme = marka.cprobs['C1']['effect']
        pprint(rme)
        self.assertTrue(0.5)

    def test_wt_effect(self):
        marka = MarkovAttribution(test_data, sep)
        wte = marka.cprobs['C1']['weighted']
        pprint(wte)
        self.assertTrue(0.2)

if __name__ == '__main__':
    unittest.main()
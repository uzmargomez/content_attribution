import unittest
from numpy import matrix, array_equal, allclose
from markov_attribution import MarkovDB

test_data = [
    {"conversion": 1, "value": 1000.00, "path": "C1 > C2 > C3"},
    {"conversion": 0, "value": 0, "path": "C1"},
    {"conversion": 0, "value": 0, "path": "C2 > C3"},
]

sep = " > "


class TestMarkovDB(unittest.TestCase):
    def test_channels(self):
        comp = ["START", "C1", "C2", "C3", "NULL", "CONVERSION"]
        test_db = MarkovDB(test_data, sep)
        test = test_db.unique_channels
        self.assertTrue(array_equal(comp, test))

    def test_probability(self):
        test_db = MarkovDB(test_data, sep)
        test = test_db.get_probability("START", "CONVERSION")
        comp = 33
        self.assertTrue(comp == round(test * 100))


if __name__ == "__main__":
    unittest.main()

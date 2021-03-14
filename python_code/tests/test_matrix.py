import unittest
from numpy import matrix, array_equal, allclose
from markov_attribution import MarkovMatrix

test_values = [
    [1, 0, 0, 0, 0],
    [1 / 2, 0, 1 / 2, 0, 0],
    [0, 1 / 2, 0, 1 / 2, 0],
    [0, 0, 1 / 2, 0, 1 / 2],
    [0, 0, 0, 0, 1],
]


class TestMarkovMatrix(unittest.TestCase):
    def standard_form(self):
        comp_values = [
            [0, 1 / 2, 0, 1 / 2, 0],
            [1 / 2, 0, 1 / 2, 0, 0],
            [0, 1 / 2, 0, 0, 1 / 2],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
        ]
        comp = matrix(comp_values)
        test_matrix = MarkovMatrix(test_values)
        test = test_matrix.standard_matrix
        print(type(comp))
        print(type(test))
        self.assertTrue(array_equal(comp, test))

    def test_q(self):
        comp_values = [[0, 1 / 2, 0], [1 / 2, 0, 1 / 2], [0, 1 / 2, 0]]
        comp = matrix(comp_values)
        test_matrix = MarkovMatrix(test_values)
        test = test_matrix.q
        print(type(comp))
        print(type(test))
        self.assertTrue(array_equal(comp, test))

    def test_n(self):
        comp_values = [[3 / 2, 1, 1 / 2], [1, 2, 1], [1 / 2, 1, 3 / 2]]
        comp = matrix(comp_values)
        test_matrix = MarkovMatrix(test_values)
        test = test_matrix.n
        print(comp)
        print(test)
        self.assertTrue(allclose(comp, test))

    def test_r(self):
        comp_values = [[1 / 2, 0], [0, 0], [0, 1 / 2]]
        comp = matrix(comp_values)
        test_matrix = MarkovMatrix(test_values)
        test = test_matrix.r
        print(type(comp))
        print(type(test))
        self.assertTrue(array_equal(comp, test))

    def test_m(self):
        comp_values = [[3 / 4, 1 / 4], [1 / 2, 1 / 2], [1 / 4, 3 / 4]]
        comp = matrix(comp_values)
        test_matrix = MarkovMatrix(test_values)
        test = test_matrix.m
        print(comp)
        print(test)
        self.assertTrue(allclose(comp, test))

    def test_absorption_states(self):
        test_matrix = MarkovMatrix(test_values)
        test = test_matrix.absorption_states
        print(test)
        self.assertTrue(test == [0, 4])

    def test_get_probability(self):
        test_matrix = MarkovMatrix(test_values)
        test = test_matrix.get_probability(1, 0)
        print(test)
        self.assertTrue(test == 3 / 4)


if __name__ == "__main__":
    unittest.main()

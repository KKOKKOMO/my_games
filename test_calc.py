import unittest
from calc import Calculator


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_sum(self):
        cases = [
            {
                'first': 10,
                'second': 2,
                'expected': 12,
            },
            {
                'first': -12,
                'second': 2,
                'expected': -10,
            },
            {
                'first': 0,
                'second': 0,
                'expected': 0,
            },
            {
                'first': 1949124,
                'second': 1237736,
                'expected': 3186860,
            },
            {
                'first': -1,
                'second': 0,
                'expected': -1,
            },
            {
                'first': -5,
                'second': 12,
                'expected': 7,
            },
        ]
        for case in cases:
            first = case['first']
            second = case['second']
            self.assertEqual(case['expected'], self.calc.sum(first, second))

    def test_sub(self):
        self.assertEqual(10, self.calc.sub(100, 90))
    

if __name__ == '__main__':
    unittest.main()
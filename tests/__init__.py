import unittest

from sample import *


class TestSimple(unittest.TestCase):

    def test_something(self):
        self.assertEqual(min(5, 6), 5)


if __name__ == '__main__':
    unittest.main()

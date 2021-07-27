from tkinter import E
from library.Border import Border
from library.PriceMovementEnum import PriceMovement
from library.BorderParser import BorderParser
import pandas as pd
import unittest


class TestBorderCompareAndParserMethod(unittest.TestCase):

    def test_equal_borders_true(self):
        first_border_left = [PriceMovement.UP, PriceMovement.UP]
        first_border_right = [PriceMovement.DOWN, PriceMovement.DOWN]

        first_border = Border(first_border_left, first_border_right)

        second_border_left = [PriceMovement.UP, PriceMovement.UP]
        second_border_right = [PriceMovement.DOWN, PriceMovement.DOWN]

        second_border = Border(second_border_left, second_border_right)

        actual = first_border.compare_borders(second_border)
        expected = True

        self.assertEqual(actual, expected)

    def test_not_equal_borders_false(self):
        first_border_left = [PriceMovement.UP, PriceMovement.UP]
        first_border_right = [PriceMovement.DOWN, PriceMovement.DOWN]

        first_border = Border(first_border_left, first_border_right)

        second_border_left = [PriceMovement.UP, PriceMovement.UP]
        second_border_right = [PriceMovement.UP, PriceMovement.DOWN]

        second_border = Border(second_border_left, second_border_right)

        actual = first_border.compare_borders(second_border)
        expected = False

        self.assertEqual(actual, expected)

    def test_border_parser_true(self):
        timeseries = pd.Series(data=[1, 2, 3, 4, 5, 2, 1, 0])
        border_parser = BorderParser(timeseries)

        actual = border_parser.get_content()
        expected = Border(left_border=[PriceMovement.UP, PriceMovement.UP],
                            right_border=[PriceMovement.DOWN, PriceMovement.DOWN])

        self.assertEqual(actual.compare_borders(expected), True)

    def test_border_parser_false(self):
        timeseries = pd.Series(data=[3, 2, 3, 4, 5, 2, 1, 0])
        border_parser = BorderParser(timeseries)

        actual = border_parser.get_content()
        expected = Border(left_border=[PriceMovement.UP, PriceMovement.UP],
                            right_border=[PriceMovement.DOWN, PriceMovement.DOWN])

        self.assertEqual(actual.compare_borders(expected), False)


if __name__ == '__main__':
    unittest.main()
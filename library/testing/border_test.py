from library.StockPriceDataFrame import StockPriceDataFrame
from tkinter import E
from library.Border import Border
from library.PriceMovementEnum import PriceMovement
from library.BorderParser import BorderParser
from library.StockPriceBorderParser import StockPriceBorderParser, StockPriceDataFrame
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

    def test_stock_price_border_parser_true(self):
        data = [{'Date': 1294012800, 'Open': 13, 'High': 100, 'Low': 20, 'Close': 15}, 
                {'Date': 1294014600, 'Open': 15, 'High': 100, 'Low': 20, 'Close': 18}, 
                {'Date': 1294016400, 'Open': 13, 'High': 100, 'Low': 20, 'Close': 14},
                {'Date': 1294018200, 'Open': 13, 'High': 100, 'Low': 20, 'Close': 14},
                {'Date': 1294020000, 'Open': 13, 'High': 100, 'Low': 20, 'Close': 14},
                {'Date': 1294021800, 'Open': 18, 'High': 100, 'Low': 20, 'Close': 14},
                {'Date': 1294023600, 'Open': 20, 'High': 100, 'Low': 20, 'Close': 14}]
        stock_price = pd.DataFrame.from_dict(data)
        stock_price = StockPriceDataFrame(stock_price)

        border_parser = StockPriceBorderParser(stock_price.get_content())

        actual = border_parser.get_content()
        expected = Border(left_border=[PriceMovement.UP, PriceMovement.UP],
                            right_border=[PriceMovement.DOWN, PriceMovement.DOWN])

        self.assertEqual(actual.compare_borders(expected), True)


if __name__ == '__main__':
    unittest.main()
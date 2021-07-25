from numpy import int32
from library.PatternHierarchyTree.Pattern import Pattern
from library.StockPriceDataFrame import StockPriceDataFrame
import pandas as pd


class StockPricePattern(Pattern):
    

    def __init__(self, stock_price_pattern: StockPriceDataFrame) -> None:
        self.stock_price_pattern: pd.DataFrame = stock_price_pattern.get_content()
        self.pattern_length: int = self.stock_price_pattern
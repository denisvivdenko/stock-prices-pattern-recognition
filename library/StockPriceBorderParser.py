from library.Border import Border
from library.PriceMovementEnum import PriceMovement
from library.StockPriceDataFrame import StockPriceDataFrame
import pandas as pd
from typing import List


class StockPriceBorderParser:


    def __init__(self, stock_price_data: pd.DataFrame, border_width=2) -> None:
        self._parsed_border = self.__parse_stock_price_border(stock_price_data, border_width)

    def get_content(self) -> Border:
        return self._parsed_border

    def __parse_stock_price_border(self, stock_price_data: pd.DataFrame, border_width) -> Border:        
        upper_bound = stock_price_data.head(border_width)
        lower_bound = stock_price_data.tail(border_width)

        left_border = self.__parse_stock_price_movement(upper_bound)
        right_border = self.__parse_stock_price_movement(lower_bound)

        return Border(left_border=left_border, right_border=right_border)

    def __parse_stock_price_movement(self, stock_price_data: pd.DataFrame) -> List[PriceMovement]:
        price_movement = []

        for index, stock_price in stock_price_data.iterrows():
            if stock_price['Open'] <= stock_price['Close']:
                price_movement.append(PriceMovement.UP)
            else:
                price_movement.append(PriceMovement.DOWN)

        return price_movement

        
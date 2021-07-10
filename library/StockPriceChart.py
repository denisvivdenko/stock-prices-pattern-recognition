import mplfinance as fplt
import pandas as pd
import numpy as np


class StockPriceChart:

    def __init__(self, stock_price_data):
        self.stock_price_data = stock_price_data


    def save_chart_image(self, file_path):
        fplt.plot(self.stock_price_data, type='candle', savefig=file_path)
        print('file has been saved: ', file_path)


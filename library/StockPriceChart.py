import mplfinance as fplt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


class StockPriceChart:

    def __init__(self, stock_price_data):
        self.stock_price_data = stock_price_data


    def save_chart_image(self, file_path):
        figure = fplt.plot(self.stock_price_data, type='candle', returnfig=True, savefig=file_path)
        print('file has been saved: ', file_path)
        matplotlib.use("Agg")
        plt.close('all')
        del figure


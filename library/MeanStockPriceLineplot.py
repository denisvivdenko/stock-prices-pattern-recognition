import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


class MeanStockPriceLinePlot:

    def __init__(self, stock_prices, linewidth=5):
        self.stock_prices = stock_prices
        self.linewidth = linewidth


    def save_chart_image(self, file_path):
        mean_stock_prices = self.stock_prices.mean(axis=1)

        figure = plt.plot(mean_stock_prices.index, mean_stock_prices.values, linewidth=self.linewidth)
        plt.savefig(file_path)
        plt.xticks(rotation=45)

        print('file has been saved: ', file_path)
        
        matplotlib.use("Agg")
        plt.close('all')

        del figure

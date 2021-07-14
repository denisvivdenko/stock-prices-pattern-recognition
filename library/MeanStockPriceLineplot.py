from library.Chart import Chart
import matplotlib.pyplot as plt


class MeanStockPriceLinePlot(Chart):

    def __init__(self, stock_prices, linewidth=5):
        super().__init__()
        self.stock_prices = stock_prices
        self.linewidth = linewidth


    def save_chart_image(self, file_path):
        mean_stock_prices = self.stock_prices.mean(axis=1)

        plt.xticks(rotation=45)
        figure = plt.plot(mean_stock_prices.index, mean_stock_prices.values, linewidth=self.linewidth)
        
        super().save_plot(file_path=file_path, figure=figure)

from library.Plot import Plot
import matplotlib.pyplot as plt


class MeanStockPriceLinePlot(Plot):


    def __init__(self, data=None, linewidth=5):
        self.plot = super().__init__(data)
        self.linewidth = linewidth

    def set_data(self, new_data):
        return MeanStockPriceLinePlot(new_data)

    def save_plot(self, file_path):
        
        mean_stock_prices = self.plot.data.mean(axis=1)

        plt.xticks(rotation=45)
        figure = plt.plot(mean_stock_prices.index, mean_stock_prices.values, linewidth=self.linewidth)
        plt.savefig(file_path)

        self.plot.remove_garbage(figure)

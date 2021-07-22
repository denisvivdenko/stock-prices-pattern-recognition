from library.Plot import Plot
import mplfinance as fplt


class StockPriceChart(Plot):


    def __init__(self, data=None):
        self.plot = super().__init__(data)


    def set_data(self, new_data):
        return StockPriceChart(new_data)


    def save_plot(self, file_path):
        figure = fplt.plot(self.plot.data, type='candle', returnfig=True, savefig=file_path)
        self.plot.remove_garbage(figure)

        


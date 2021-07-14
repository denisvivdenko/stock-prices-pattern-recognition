from library.Chart import Chart
import mplfinance as fplt
import matplotlib.pyplot as plt


class StockPriceChart(Chart):

    def __init__(self, stock_price_data):
        super().__init__()
        self.stock_price_data = stock_price_data


    def save_chart_image(self, file_path):
        figure = fplt.plot(self.stock_price_data, type='candle', 
                            returnfig=True, savefig=file_path)
        super().__remove_garbage(figure)

        


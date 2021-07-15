import matplotlib
from library.Window import Window
from library.WindowsGroupLinker import WindowsGroupLinker
from library.RepeatsHandler import RepeatsHandler
from library.MeanStockPriceLineplot import MeanStockPriceLinePlot
from library.StockPriceChart import StockPriceChart
import pandas as pd
import sqlite3
from library.StockPriceDataFrame import StockPriceDataFrame
from library.Plot import Plot
import os


def save_plots(data: dict, plot: Plot):

    count = 0
    for pattern_class, windows in data.items():

        folder_name = 'charts\\class_' + str(pattern_class)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for window in windows:

            first_timestamp = str(int(window.index[0].timestamp()))
            file_path = folder_name + '\\chart_' + first_timestamp + '.png'

            window_plot = plot.set_data(window)
            window_plot.save_plot(file_path)

            count += 1
            print('total', str(count))




if __name__ == '__main__':

    connection = sqlite3.connect('./data/GBPUSD.db')
    groups_info = pd.read_sql_query("SELECT * FROM result_table_2010", connection, parse_dates=True)
    groups_info = groups_info.rename({'time_name_pattern': 'timestamp', 'numClass': 'class'}, axis=1)
    index = pd.to_datetime(groups_info.timestamp, unit='s')
    groups_info = groups_info.drop('timestamp', axis=1)
    groups_info.index = index

    price_data = pd.read_sql_query('SELECT pTime, pOpen, pHigh, pLow, pClose FROM d_2010', connection, parse_dates=True)
    price_data = StockPriceDataFrame(price_data).get_content()

    connection.close()

    timestamps_period = 30*60
    repeats_handler = RepeatsHandler(timestamps_period=timestamps_period)
    cleaned_groups_info = repeats_handler.clear_repeats(groups_info)

    windows = [Window(price_data, timestamp, candles_number=20) for timestamp in cleaned_groups_info.index]
    windows_group_linker = WindowsGroupLinker(cleaned_groups_info, windows)

    linked_windows_groups = windows_group_linker.get_content()
    
    save_plots(linked_windows_groups, MeanStockPriceLinePlot())
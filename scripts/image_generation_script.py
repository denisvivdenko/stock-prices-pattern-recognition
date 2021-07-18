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
import click


@click.command()
@click.option('--d1')
@click.option('--t1')
@click.option('--t1_time_col')
@click.option('--t1_class_col')
@click.option('--d2')
@click.option('--t2')
@click.option('--t2_time_col', default='Timestamp')
@click.option('--t2_open_col', default='Open')
@click.option('--t2_high_col', default='High')
@click.option('--t2_low_col', default='Low')
@click.option('--t2_close_col', default='Close')
@click.option('--candles', default=20)
@click.option('--timestamp_period', default=30*60)
@click.option('--save')
def run_script(d1, t1, t1_time_col, t1_class_col,
                d2, t2, t2_time_col, t2_open_col,
                t2_high_col, t2_low_col, t2_close_col, 
                candles, timestamp_period, save):

    db1_connection = sqlite3.connect(d1)
    groups_info = pd.read_sql_query(f"SELECT * FROM {t1}", db1_connection, parse_dates=True)
    groups_info = groups_info.rename({t1_time_col: 'timestamp', t1_class_col: 'class'}, axis=1)
    index = pd.to_datetime(groups_info.timestamp, unit='s')
    groups_info = groups_info.drop('timestamp', axis=1)
    groups_info.index = index
    db1_connection.close()

    db2_connection = sqlite3.connect(d2)
    price_data = pd.read_sql_query(f'SELECT {t2_time_col}, {t2_open_col}, {t2_high_col}, {t2_low_col}, {t2_close_col} FROM {t2}', db2_connection, parse_dates=True)
    price_data = StockPriceDataFrame(price_data).get_content()
    db2_connection.close()

    repeats_handler = RepeatsHandler(timestamps_period=timestamp_period)
    cleaned_groups_info = repeats_handler.clear_repeats(groups_info)

    windows = [Window(price_data, timestamp, candles_number=candles) for timestamp in cleaned_groups_info.index]
    windows_group_linker = WindowsGroupLinker(cleaned_groups_info, windows)
    linked_windows_groups = windows_group_linker.get_content()
    
    save_plots(linked_windows_groups, StockPriceChart(), save)


def save_plots(data: dict, plot: Plot, path):

    count = int()
    for pattern_class, windows in data.items():

        folder_name ='charts\\class_' + str(pattern_class)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for window in windows:

            first_timestamp = str(int(window.index[0].timestamp()))
            file_path = folder_name + '\\chart_' + first_timestamp + '.png'

            window_plot = plot.set_data(window)
            window_plot.save_plot(file_path)

            count += 1
            print_count_info(pattern_class, count, len(windows))


def print_count_info(pattern_class, count, number_windows):
    print(f"class: {pattern_class}\tcount: {count}/{number_windows}")


if __name__ == '__main__':

    run_script()

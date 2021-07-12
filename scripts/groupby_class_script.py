from datetime import time
from library.MeanStockPriceLineplot import MeanStockPriceLinePlot
from library.StockPriceChart import StockPriceChart
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from library.ChartSegment import ChartSegment
from library.StockPriceDataFrame import StockPriceDataFrame
import os

segment_size = 20

connection = sqlite3.connect('./data/GBPUSD.db')
df = pd.read_sql_query("SELECT * FROM result_table_2010", connection, parse_dates=True)
df = df.rename({'time_name_pattern': 'timestamp', 'numClass': 'class'}, axis=1)


def save_plots(db_connection, data):

    stock_price_df = pd.read_sql_query('SELECT pTime, pOpen, pHigh, pLow, pClose FROM d_2010', db_connection, parse_dates=True)
    stock_price_df = StockPriceDataFrame(stock_price_df).get_content()

    db_connection.close()

    classes = list(set(data['class']))

    count = 0
    for pattern_class in classes:
        pattern_data = data[data['class'] == pattern_class]
        timestamps_data = list(set(pattern_data.timestamp))

        folder_name = 'charts\\class_' + str(pattern_class)

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for timestamp in timestamps_data:
            start_date = pd.to_datetime(timestamp, unit='s')
    
            segment = stock_price_df[stock_price_df.index > start_date].head(segment_size)
            print(segment)

            file_name = folder_name + '\\chart_' + timestamp + '.png'

            stream = StockPriceChart(segment)
            stream.save_chart_image(file_path=file_name) 

            # stream = MeanStockPriceLinePlot(segment, linewidth=10)
            # stream.save_chart_image(file_name)

            count += 1
            print('total', str(count))


if __name__ == '__main__':
    pass
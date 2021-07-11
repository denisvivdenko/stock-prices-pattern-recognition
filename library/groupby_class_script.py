from datetime import time

from numpy.core.numeric import count_nonzero
from StockPriceChart import StockPriceChart
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from ChartSegment import ChartSegment
from StockPriceDataFrame import StockPriceDataFrame
import os

segment_size = 20

connection = sqlite3.connect('./data/GBPUSD.db')
df = pd.read_sql_query("SELECT * FROM result_table_2010", connection, parse_dates=True)
df = df.rename({'time_name_pattern': 'timestamp', 'numClass': 'class'}, axis=1)

stock_price_df = pd.read_sql_query('SELECT pTime, pOpen, pHigh, pLow, pClose FROM d_2010', connection, parse_dates=True)
stock_price_df = StockPriceDataFrame(stock_price_df).get_content()

connection.close()

classes = list(set(df['class']))

count = 0
for pattern_class in classes:
    pattern_data = df[df['class'] == pattern_class]
    timestamps_data = list(set(pattern_data.timestamp))

    folder_name = 'charts\\class_' + str(pattern_class)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for timestamp in timestamps_data:
        start_date = pd.to_datetime(timestamp, unit='s')
        # end_date = str(pd.to_datetime(str(int(timestamp) + 19 * 30 * 60), unit='s'))

        # segment = ChartSegment(stock_price_df, start_date=start_date, end_date=end_date,
        #             frequency='30T')
 
        segment = stock_price_df[stock_price_df.index > start_date].head(segment_size)
        print(segment)

        file_name = folder_name + '\\chart_' + timestamp + '.png'

        stream = StockPriceChart(segment)
        stream.save_chart_image(file_path=file_name) 

        count += 1
        print('total', str(count))

from StockPriceChart import StockPriceChart
from ChartSegment import ChartSegment
from StockPriceDataFrame import StockPriceDataFrame
import sqlite3
import pandas as pd

pd.set_option('display.max_rows', 2000)

connection = sqlite3.connect("./data/GBPUSD.db")

cursor = connection.cursor()

count = 0
date = []
open = [] 
high = [] 
low = [] 
close = []

for row in cursor.execute('SELECT pTime, pOpen, pHigh, pLow, pClose FROM d_2010;'):
    date.append(row[0])
    open.append(row[1])
    high.append(row[2])
    low.append(row[3])
    close.append(row[4])

connection.close()


price_dateframe = StockPriceDataFrame(date, open=open, high=high, low=low, close=close)
print(price_dateframe.get_content())

segmentation = ChartSegment(price_dateframe.get_content(), 
    start_date='2010.01.07 13:30', end_date='2010.01.10 08:30')
print(segmentation.get_content())

chart = StockPriceChart(segmentation.get_content())
file_path = 'chart1.png'
chart.save_chart_image(file_path=file_path)
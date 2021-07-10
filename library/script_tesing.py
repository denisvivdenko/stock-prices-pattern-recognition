from ChartSegment import ChartSegment
from StockPriceDataFrame import StockPriceDataFrame
import sqlite3


connection = sqlite3.connect("./data/GBPUSD.db")

cursor = connection.cursor()

count = 0
date = []
open = [] 
high = [] 
low = [] 
close = []

for row in cursor.execute('SELECT * FROM MT4__M00030;'):
    if count == 20:
        break
    
    date.append(row[0])
    open.append(row[1])
    high.append(row[2])
    low.append(row[3])
    close.append(row[4])
    
    count += 1

connection.close()


price_dateframe = StockPriceDataFrame(date, open=open, high=high, low=low, close=close)
print(price_dateframe.get_content())

segmentation = ChartSegment(price_dateframe.get_content(), start_date='2001-01-03 01:00:00', end_date='2001-01-03 07:00:00')
print(segmentation.get_content())
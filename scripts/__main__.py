import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from library.StockPriceDataFrame import StockPriceDataFrame
from library.MotifsFinder import MotifsFinder


if __name__ == '__main__':
    connection = sqlite3.connect('./data/GBPUSD.db')
    stock_prices = pd.read_sql_query(f"SELECT * FROM d_2010", connection, parse_dates=True)
    connection.close()

    columns = ['pTime', 'pOpen', 'pHigh', 'pLow', 'pClose']
    stock_prices = StockPriceDataFrame(stock_prices[columns]).get_content()

    one_dimension_timeseries = stock_prices.mean(axis=1)

    motifs_finder = MotifsFinder(one_dimension_timeseries, 20, correlation_threshold=0.95)

    count = 0
    count_skiped = 0
    while motifs_finder.is_next():
        motif = motifs_finder.get_motif()
        
        if motif.empty:
            count_skiped += 1

        count += 1
    
    print(f'{count_skiped}/{count}')

        

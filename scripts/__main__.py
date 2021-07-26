from sklearn.preprocessing import normalize
from operator import index
from library.MotifsRecursiveMerger import MotifsRecursiveMerger
import pandas as pd
import sqlite3
import numpy as np
import os
import matplotlib.pyplot as plt
from library.StockPriceDataFrame import StockPriceDataFrame
from library.MotifsFinder import MotifsFinder
from library.PatternGeneralizer import PatternGeneralizer
from library.StockPriceChart import StockPriceChart


if __name__ == '__main__':
    connection = sqlite3.connect('./data/GBPUSD.db')
    stock_prices = pd.read_sql_query(f"SELECT * FROM d_2010", connection, parse_dates=True)
    test_dataset = pd.read_sql_query(f"SELECT * FROM d_2011", connection, parse_dates=True)
    connection.close()

    columns = ['pTime', 'pOpen', 'pHigh', 'pLow', 'pClose']
    stock_prices = StockPriceDataFrame(stock_prices[columns]).get_content()
    test_dataset = StockPriceDataFrame(test_dataset[columns]).get_content()

    one_dimension_timeseries = stock_prices.median(axis=1)

    motifs_finder = MotifsFinder(one_dimension_timeseries, 10, correlation_threshold=0.95)

    motifs = []
    count = 0
    while motifs_finder.is_next():
        count += 1
        motif = motifs_finder.get_motif()
        
        if not motif.empty:
            generalizer = PatternGeneralizer(motif)
            generalized_pattern = generalizer.get_content()
            motifs.append(generalized_pattern)

    recursive_merger = MotifsRecursiveMerger(motifs)
    distinct_motifs = recursive_merger.get_content()

    pattern_size = distinct_motifs[0].shape[0]

    timestamps_iter = iter(test_dataset.index)
    for pattern_timestamp in timestamps_iter:

        pattern = test_dataset[test_dataset.index > pattern_timestamp].head(pattern_size)
        
        ma_pattern = pattern.median(axis=1)
        ma_pattern = pd.Series(index=pd.RangeIndex(start=0, stop=pattern_size),
                                data=normalize([ma_pattern])[0])
        
        class_identifier = 0
        for classified_pattern in distinct_motifs:
            correlation = classified_pattern.corr(ma_pattern, method='pearson')
            class_identifier += 1

            if correlation >= 0.95:
                stock_price_chart = StockPriceChart(pattern)
                
                folder_name = './charts/class_' + str(class_identifier)
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                    plt.plot(classified_pattern)
                    plt.savefig(folder_name + '/general_pattern.png')
                    plt.close()

                stock_price_chart.save_plot(folder_name + f'/pattern_{int(pattern_timestamp.timestamp())}')
                print(f'pattern: {pattern_timestamp} is {class_identifier}') 

                [next(timestamps_iter) for n in range(int(np.ceil(pattern_size / 4)))]

                break 
                      

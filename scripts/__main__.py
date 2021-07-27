from library.StockPriceBorderParser import StockPriceBorderParser
from typing import Pattern
from library.MotifsRecursiveMerger import MotifsRecursiveMerger
from library.StockPriceDataFrame import StockPriceDataFrame
from library.MotifsFinder import MotifsFinder
from library.PatternGeneralizer import PatternGeneralizer
from library.StockPriceChart import StockPriceChart
from library.Border import Border
from library.BorderParser import BorderParser
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import numpy as np
import os


def save_classified_pattern(general_pattern, pattern, class_identifier, pattern_first_timestamp):
    stock_price_chart = StockPriceChart(pattern)
            
    folder_name = './charts/class_' + str(class_identifier)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        plt.plot(general_pattern)
        plt.savefig(folder_name + '/general_pattern.png')
        plt.close()

    stock_price_chart.save_plot(folder_name + f'/pattern_{pattern_first_timestamp}')
    print(f'window: {pattern_first_timestamp} is {class_identifier}') 


if __name__ == '__main__':
    correlation_threshold = 0.95

    connection = sqlite3.connect('./data/GBPUSD.db')
    stock_prices = pd.read_sql_query(f"SELECT * FROM d_2010", connection, parse_dates=True)
    test_dataset = pd.read_sql_query(f"SELECT * FROM d_2011", connection, parse_dates=True)
    connection.close()

    columns = ['pTime', 'pOpen', 'pHigh', 'pLow', 'pClose']
    stock_prices = StockPriceDataFrame(stock_prices[columns]).get_content()
    test_dataset = StockPriceDataFrame(test_dataset[columns]).get_content()

    one_dimension_timeseries = stock_prices.mean(axis=1)

    motifs_finder = MotifsFinder(one_dimension_timeseries, 12, correlation_threshold=0.95)

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
    for window_timestamp in timestamps_iter:

        window = test_dataset[test_dataset.index > window_timestamp].head(pattern_size)
        
        median_window = window.mean(axis=1)
        median_window = pd.Series(index=pd.RangeIndex(start=0, stop=pattern_size),
                                data=normalize([median_window])[0])

        window_border = StockPriceBorderParser(window).get_content()
        
        correlations = []
        border_compatibility = []
        
        for pattern in distinct_motifs:
            correlation = pattern.corr(median_window, method='pearson')
            correlations.append(correlation)

            pattern_border = BorderParser(pattern).get_content()
            border_compatibility.append(window_border.compare_borders(pattern_border))

        best_correlation_indices = np.argsort(correlations)[::-1]

        for best_correlation_index in best_correlation_indices:
            if correlations[best_correlation_index] < correlation_threshold:
                break

            if border_compatibility[best_correlation_index] == True:
                class_identifier = best_correlation_index
                
                window_first_timestamp = int(window_timestamp.timestamp())
                save_classified_pattern(distinct_motifs[best_correlation_index], 
                                        window, class_identifier, window_first_timestamp)

                [next(timestamps_iter) for n in range(int(np.ceil(pattern_size / 4)))]



            # if correlation >= 0.95:
            #     stock_price_chart = StockPriceChart(window)
                
            #     folder_name = './charts/class_' + str(class_identifier)
            #     if not os.path.exists(folder_name):
            #         os.makedirs(folder_name)
            #         plt.plot(pattern)
            #         plt.savefig(folder_name + '/general_pattern.png')
            #         plt.close()

            #     stock_price_chart.save_plot(folder_name + f'/pattern_{int(window_timestamp.timestamp())}')
            #     print(f'window: {window_timestamp} is {class_identifier}') 

            #     [next(timestamps_iter) for n in range(int(np.ceil(pattern_size / 4)))]

            #     break 
                      

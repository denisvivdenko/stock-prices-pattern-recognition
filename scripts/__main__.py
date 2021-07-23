from library.MotifsRecursiveMerger import MotifsRecursiveMerger
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from library.StockPriceDataFrame import StockPriceDataFrame
from library.MotifsFinder import MotifsFinder
from library.PatternGeneralizer import PatternGeneralizer


if __name__ == '__main__':
    connection = sqlite3.connect('./data/GBPUSD.db')
    stock_prices = pd.read_sql_query(f"SELECT * FROM d_2010", connection, parse_dates=True)
    connection.close()

    columns = ['pTime', 'pOpen', 'pHigh', 'pLow', 'pClose']
    stock_prices = StockPriceDataFrame(stock_prices[columns]).get_content()

    one_dimension_timeseries = stock_prices.mean(axis=1)

    motifs_finder = MotifsFinder(one_dimension_timeseries, 20, correlation_threshold=0.95)

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

    print(f'before merge: {len(motifs)}/{count}')
    print(f'after merge: {len(distinct_motifs)}')
    
    count = 0
    for motif in distinct_motifs:

        plt.figure(figsize=(2, 6))
        plt.plot(motif, linewidth=3)
        plt.savefig(f'./patterns/pattern_{count}')
        plt.close()
        count += 1
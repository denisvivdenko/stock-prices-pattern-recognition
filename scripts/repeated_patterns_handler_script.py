from scripts.groupby_class_script import save_plots
from library.RepeatsHandler import RepeatsHandler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import math


time_period = '30T'
timestamp_period = 30 * 60


def read_data():
    connection = sqlite3.connect('./data/GBPUSD.db')
    df = pd.read_sql_query("SELECT * FROM result_table_2010", connection, parse_dates=True)
    df = df.rename({'time_name_pattern': 'timestamp', 'numClass': 'class'}, axis=1)
    index = df.timestamp
    df = df.drop('timestamp', axis=1)
    df.index = index

    return df


if __name__ == "__main__":
    connection = sqlite3.connect('./data/GBPUSD.db')

    data = read_data()

    repeats_handler = RepeatsHandler(timestamps_period=timestamp_period)
    results = repeats_handler.clear_repeats(data)

    # save_plots(connection, results)
    print(results)

    connection.close()


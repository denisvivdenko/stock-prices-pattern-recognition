from scripts.groupby_class_script import save_plots
from sqlite3.dbapi2 import Timestamp
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
    
    return df


def get_clusters(data):

    clusters = dict()

    cluster_number = 0
    clusters[cluster_number] = list()

    previous_timestamp = data['timestamp'].values[0]
    clusters[cluster_number] = [previous_timestamp]

    for current_timestamp in data['timestamp'].values[1:]:
        if (int(current_timestamp) - int(previous_timestamp)) == timestamp_period:
            clusters[cluster_number].append(current_timestamp)
        else:
            cluster_number += 1
            clusters[cluster_number] = [current_timestamp]

        previous_timestamp = current_timestamp

    return clusters


def clear_repeated_patterns(clusters: dict):
    
    filtred_timestamps = []

    for timestamps in clusters.values():
        timestamps_count = len(timestamps)
        filtred_timestamp_index = math.ceil(timestamps_count / 2) - 1

        filtred_timestamps.append(timestamps[filtred_timestamp_index])

    return filtred_timestamps


if __name__ == "__main__":
    connection = sqlite3.connect('./data/GBPUSD.db')

    classified_data = read_data()
    patterns = list(set(classified_data['class']))

    filtred_data = []
    for pattern in patterns:

        pattern_data = classified_data[classified_data['class'] == pattern]
        clusters = get_clusters(pattern_data)
        filtred_data += clear_repeated_patterns(clusters)

    
    result = classified_data[classified_data.timestamp.isin(filtred_data)]
    save_plots(connection, result)
    print(result)


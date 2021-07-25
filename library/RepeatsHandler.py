import math
import pandas as pd


class RepeatsHandler():


    def __init__(self, timestamps_period):
        self.timestamps_period = timestamps_period

    def clear_repeats(self, data: pd.DataFrame):
        '''
        data must have: 
        "timestamp" column as its index and
        "class" column which identify class of pattern
        '''
        
        data = data.copy()
        filtred_data = []
        classes = set(data['class'])
        for class_identifier in classes:

            class_data = data[data['class'] == class_identifier]
            
            clusters = self.__get_clusters(class_data)
            filtred_data += self.__filter_repeats(clusters)

        
        clean_data = data[data.index.isin(filtred_data)]
        return clean_data.copy()

    def __filter_repeats(self, clusters: dict):
        '''filters clusters: takes the centred one timestamp from each cluster'''

        filtred_timestamps = []

        for timestamps in clusters.values():
            timestamps_count = len(timestamps)
            filtred_timestamp_index = math.ceil(timestamps_count / 2) - 1

            filtred_timestamps.append(timestamps[filtred_timestamp_index])

        return filtred_timestamps

    def __get_clusters(self, data: pd.DataFrame):
        '''data must have timestamp as its index'''

        data = data.copy()
        clusters = dict()

        cluster_number = 0
        clusters[cluster_number] = list()

        previous_timestamp = data.index[0]
        clusters[cluster_number] = [previous_timestamp]

        for current_timestamp in data.index[1:]:

            timestamps_difference = current_timestamp.timestamp() - previous_timestamp.timestamp()

            if timestamps_difference == self.timestamps_period:
                clusters[cluster_number].append(current_timestamp)
            else:
                cluster_number += 1
                clusters[cluster_number] = [current_timestamp]

            previous_timestamp = current_timestamp

        return clusters




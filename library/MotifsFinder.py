import pandas as pd
import numpy as np
import stumpy
from sklearn.preprocessing import normalize
from library.MotifsMerger import MotifsMerger


class MotifsFinder:


    def __init__(self, timeseries: pd.Series, window_size, correlation_threshold=0.9):
        self.current_motif_index = -1
        self.timeseries = timeseries
        self.window_size = window_size
        self.correlation_threshold = correlation_threshold
        self.matrix_profile = stumpy.stump(timeseries, m=window_size)
        self.motif_indices = np.argsort(self.matrix_profile[:, 0])
        self.previous_correlation = 1

    def get_motif(self):

        # step by 2 is connected with matrix profile realization
        self.current_motif_index += 2  

        if self.current_motif_index > self.timeseries.size - 1:
            raise Exception('MotifsFinder: index is out of range')

        if self.previous_correlation < self.correlation_threshold:
            return pd.Series()

        motifs, correlation = self.__get_pairwised_motif(self.current_motif_index)
        self.previous_correlation = correlation
        
        motifs_merger = MotifsMerger(motifs)
        merged_motif = motifs_merger.get_content()

        return merged_motif

    def is_next(self):
        if (self.current_motif_index+2) < (self.timeseries.size-1):
            return True

        return False

    def __get_pairwised_motif(self, motif_index):

        timeseries_motif_index = self.motif_indices[motif_index]
        nearest_neighbor_index = self.matrix_profile[timeseries_motif_index, 1]

        index = pd.RangeIndex(0, self.window_size)

        first_motif = self.timeseries[timeseries_motif_index:].head(self.window_size)
        second_motif = self.timeseries[nearest_neighbor_index:].head(self.window_size)

        normalized_first_motif = pd.Series(data=normalize([first_motif])[0], index=index)
        normalized_second_motif = pd.Series(data=normalize([second_motif])[0], index=index)

        correlation = normalized_first_motif.corr(normalized_second_motif, method='pearson')

        return [normalized_first_motif, normalized_second_motif], correlation

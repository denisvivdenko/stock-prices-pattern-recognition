import pandas as pd
from library.MotifsMerger import MotifsMerger
import time


class MotifsRecursiveMerger:

    def __init__(self, motifs:list, correlation_threshold=0.95):
        self.distinct_motifs = self.__get_distinct_motifs(motifs, correlation_threshold)


    def get_content(self):
        return self.distinct_motifs


    def __get_distinct_motifs(self, motifs, correlation_threshold):
        distinct_motifs = motifs.copy()
        
        start_time = time.time()
        while self.__check_correlated_motifs(distinct_motifs, correlation_threshold):
            end_time = time.time() - start_time
            print(f'check correlation {end_time}s.')

            start_time = time.time()
            distinct_motifs = self.__merge_correlated_motifs(distinct_motifs, correlation_threshold)

            end_time = time.time() - start_time
            print(f'merge correlated motifs {end_time}s.')

        return distinct_motifs



    def __check_correlated_motifs(self, motifs, correlation_threshold):

        motifs_count = len(motifs)

        for y_index in range(motifs_count):

            for x_index in range(y_index):
                motifs_pair_correlation = motifs[y_index].corr(motifs[x_index], method='pearson')

                if motifs_pair_correlation > correlation_threshold:
                    return True

        return False


    def __merge_correlated_motifs(self, motifs, correlation_threshold):

        motifs_count = len(motifs)

        result_motifs = list()
        for y_index in range(motifs_count):
            is_distinct = True

            for x_index in range(y_index):
                motifs_pair_correlation = motifs[y_index].corr(motifs[x_index], method='pearson')

                if motifs_pair_correlation > correlation_threshold:
                    motifs_merger = MotifsMerger([motifs[y_index], motifs[x_index]])
                    result_motifs.append(motifs_merger.get_content())
                    is_distinct = False
            
            if is_distinct:
                result_motifs.append(motifs[y_index])

        return result_motifs

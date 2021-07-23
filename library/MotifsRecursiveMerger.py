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
            start_time = time.time()

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
        motifs = motifs.copy()
        result_motifs = list()
        removed_indices = list()
        motifs_count = len(motifs)

        for current_motif_index in range(motifs_count):
            
            if current_motif_index in removed_indices:
                continue
            
            current_motif = motifs[current_motif_index]
            is_ditinct = True

            for second_motif_index in range(current_motif_index + 1, motifs_count):

                if second_motif_index in removed_indices:
                    continue

                second_motif = motifs[second_motif_index]
                motifs_correlation = current_motif.corr(second_motif, method='pearson')

                if motifs_correlation >= correlation_threshold:
                    motifs_merger = MotifsMerger([current_motif, second_motif])
                    merged_motif = motifs_merger.get_content()

                    removed_indices.append(current_motif_index)
                    removed_indices.append(second_motif_index)

                    result_motifs.append(merged_motif)
                    is_ditinct = False
                    break

            if is_ditinct:
                result_motifs.append(current_motif)

        print(len(result_motifs))
        return result_motifs

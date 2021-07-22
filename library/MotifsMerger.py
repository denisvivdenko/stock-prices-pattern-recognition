class MotifsMerger:

    def __init__(self, motifs: list):
        self.merged_motifs = self.__merge_motifs(motifs=motifs)

    
    def get_content(self):
        return self.merged_motifs

    
    def __merge_motifs(self, motifs):

        merged_motif = motifs[0]

        for current_motif in motifs[1:]:
            merged_motif = (merged_motif + current_motif) / 2

        return merged_motif
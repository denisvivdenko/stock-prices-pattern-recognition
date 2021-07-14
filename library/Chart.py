from math import inf
import matplotlib.pyplot as plt
import matplotlib


class Chart:

    def __init__(self):
        matplotlib.use("Agg")
        return self

    
    def save_plot(self, file_path, figure, info=False):
        plt.savefig(file_path)

        if info:
            print('file has been saved: ', file_path)


    def remove_garbage(self, figure):
        del figure
        plt.close('all')

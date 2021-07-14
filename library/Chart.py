from math import inf
import matplotlib.pyplot as plt
import matplotlib


class Chart:

    def __init__(self):
        matplotlib.use("Agg")

    
    def save_plot(self, file_path, figure, info=False):
        plt.savefig(file_path)
        self.__remove_garbage(figure)

        if info:
            print('file has been saved: ', file_path)


    def __remove_garbage(self, figure):
        del figure
        plt.close('all')

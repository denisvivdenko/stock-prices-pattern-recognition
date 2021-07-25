import matplotlib.pyplot as plt
import matplotlib


class Plot:


    def __init__(self, data):
        self.data = data
        self.__set_use_settings()
        return self

    def set_data(self, new_data):
        return Plot(new_data)

    def save_plot(self):
        pass

    def remove_garbage(self, figure):
        del figure
        plt.close('all')

    def __set_use_settings(self, use="Agg"):
        if matplotlib.get_backend() != use:
            matplotlib.use(use)



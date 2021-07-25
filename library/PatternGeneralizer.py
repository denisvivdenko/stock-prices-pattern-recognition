from matplotlib.pyplot import axis
import pandas as pd
import math


class PatternGeneralizer:


    def __init__(self, timeseries: pd.Series, smoothing_coefficient=0.2):
        self.generalized_pattern = self.smooth_timeseries(timeseries, smoothing_coefficient)

    def get_content(self):
        return self.generalized_pattern
    
    def smooth_timeseries(self, timeseries: pd.Series, smoothing_coefficient):
        window_size = timeseries.size
        smoothing_window = int(math.ceil(window_size * smoothing_coefficient))
        smoothed_timeseries = timeseries.rolling(window=smoothing_window).mean()

        smoothed_timeseries = smoothed_timeseries.dropna()
        smoothed_timeseries.index = pd.RangeIndex(0, window_size - smoothing_window + 1)

        return smoothed_timeseries

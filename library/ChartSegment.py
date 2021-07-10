import pandas as pd
import numpy as np
from pandas.core.indexes.datetimes import date_range
import mplfinance as fplt
import sqlite3


class ChartSegment:

    def __init__(self, data: pd.DataFrame, start_date, end_date, frequency='T'):
        self.__time_segment = self.__get_time_segment(data, start_date, end_date, frequency)


    def get_content(self):
        return self.__time_segment


    def __get_time_segment(self, data, start_date, end_date, frequency):
        date_range = pd.date_range(start=start_date, end=end_date, freq=frequency)
        time_segment = data[data.index.isin(date_range)]

        return time_segment
    
    
import pandas as pd
import numpy as np


class StockPriceDataFrame:

    def __init__(self, date, open, high, low, close, volume=[]):
        self.__price_dataframe = self.__initialize_dateframe(date, open, high, low, close, volume)


    def get_content(self):
        return self.__price_dataframe

    
    def __initialize_dateframe(self, date, open, high, low, close, volume=[]):
        is_volume = False

        date = pd.Series(date, name='Date')
        if not self.__is_datetime_format(date):
            date = pd.to_datetime(date, unit='s')

        data = np.stack((open, high, low, close), axis=1)
        columns = ['Open', 'High', 'Low', 'Close']
        if volume:
            data.append(volume)
            columns.append('Volume')
            is_volume = True


        price_data = pd.DataFrame(data=data, index=date, columns=columns)
        return price_data


    def __is_datetime_format(self, date):
        if type(date) is not pd.core.indexes.datetimes.DatetimeIndex:
            
            return False

        return True
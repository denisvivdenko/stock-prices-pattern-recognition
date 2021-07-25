import pandas as pd


class Window:


    def __init__(self, data: pd.DataFrame, first_timestamp, candles_number=20):
        '''param data: must have timestamp as index'''

        self._window = self.__get_window(data, first_timestamp, candles_number)

    def get_content(self):
        return self._window

    def __get_window(self, data, first_timestamp, candles_number):
        
        data = data.copy()
        window = data[data.index >= pd.to_datetime(first_timestamp, unit='s')].head(candles_number)

        if window.shape[0] < candles_number:
            raise Exception('window length is less than specified candles number')

        return window
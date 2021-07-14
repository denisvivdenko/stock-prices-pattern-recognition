import pandas as pd


class WindowsGroupLinker:

    def __init__(self, groups_info: pd.DataFrame, windows: list):
        '''
        param groups: groups data with "timestamp" column as index and "class" column as class identifier
        param windows: list of windows that have to be linked to a particular group
        '''

        self.grouped_windows = self.__group_windows(groups_info=groups_info, windows=windows)


    def get_content(self):
        return self.grouped_windows

    
    def __group_windows(self, groups_info, windows):
        groups_info = groups_info.copy()

        groups = set(groups_info['class'])
        grouped_data = {group : list() for group in groups}
        
        for window in windows:
            window_data = window.get_content()
            window_first_timestamp = window_data.index[0]

            window_group = groups_info.loc[groups_info.index == window_first_timestamp, 'class']

            grouped_data[window_group] = window_data

        return grouped_data


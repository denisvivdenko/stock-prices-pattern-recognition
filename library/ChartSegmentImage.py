import pandas as pd
import numpy as np
import mplfinance as fplt
import sqlite3


class ChartSegmentImage:

    def __init__(self, data: pd.DataFrame, start_date, end_date):
        self.data = data
        self.start_date = start_date
        self.end_date = end_date

    
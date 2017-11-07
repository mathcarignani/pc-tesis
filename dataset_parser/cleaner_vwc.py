from cleaner_vwc_headers import HEADERS
import pandas as pd
import datetime as dt


class CleanerVWC:
    FIRST_TIMESTAMP = '2010-10-01 00:00:00'
    LAST_TIMESTAMP = '2013-10-01 00:00:00'
    NO_DATA = 'NULL'  # missing data

    def __init__(self, dirty_df, filename):
        self.df = dirty_df
        self.filename = CleanerVWC._fix_filename(filename)
        self.header = HEADERS[self.filename]
        self.header_count = len(self.header)
        self.header_index = 0

    def clean(self):
        self._fill_missing_dates()
        self._substitute_nan_values()
        self.total_lines = self.row_count + self.header_count  # used for ProgressBar

    # fill the missing dates from FIRST_TIMESTAMP until LAST_TIMESTAMP
    def _fill_missing_dates(self):
        last_ts = dt.datetime.strptime(CleanerVWC.FIRST_TIMESTAMP, "%Y-%m-%d %H:%M:%S")
        first_ts = dt.datetime.strptime(CleanerVWC.LAST_TIMESTAMP, "%Y-%m-%d %H:%M:%S")
        all_days = pd.date_range(last_ts, first_ts, freq='H')
        self.df = self.df.reindex(all_days)

    # substitute nan values with NO_DATA string
    def _substitute_nan_values(self):
        self.df = self.df.fillna(CleanerVWC.NO_DATA)
        self.row_count = len(self.df.index)
        self.row_index = 0

    # The cleaned files must have .clean.smet extension
    @classmethod
    def _fix_filename(_, filename):
        return filename.replace('.dat', '.smet').replace('.smet', '.clean.smet')

    def has_finished(self):
        return self.header_count == 0 and self.row_count == 0

    def generate_line(self):
        if self.header_count == 0:
            return self._data_line()
        else:
            return self._header_line()

    def _data_line(self):
        index = self.df.index[self.row_index]
        values = self.df.loc[index].values
        data_row = ' '.join(str(x) for x in values)
        timestamp_str = index.strftime("%Y-%m-%dT%H:%M")  # 2010-10-01T16:00
        data_row = timestamp_str + ' ' + data_row
        self.row_index += 1
        self.row_count -= 1
        return data_row

    def _header_line(self):
        header_row = self.header[self.header_index]
        self.header_index += 1
        self.header_count -= 1
        return header_row

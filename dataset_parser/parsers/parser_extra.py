import numpy as np


# class ParserExtra(object):
#     # used by IRKIS and ElNino
#     def _add_data(self, data, current_date, line, timestamp, np_array):
#         if len(data) == self.columns_count:
#             if current_date == self.last_date:
#                 self.errors['duplicate_rows'].append(line)
#             else:
#                 np_array = self._clean_data(data)
#                 self.last_date = current_date
#         else:
#             # if the line has an inconsistent number of values mark the whole row as invalid
#             self.errors['missing_values'].append(line)
#             np_array = np.array([np.nan] * len(self.df.columns))
#
#         if np_array is not None:
#             self.df.loc[timestamp] = np_array
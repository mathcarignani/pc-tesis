import sys
sys.path.append('.')

import pandas as pd
import math
import json

from pandas_tools.pandas_tools import PandasTools
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.compress.calculate_std_manual import CalculateSTDManual
from file_utils.text_utils.text_file_reader import TextFileReader
from file_utils.text_utils.text_file_writer import TextFileWriter

class CompressUtils:
    COMPARE = True
    RECORD = False
    STDS_FILENAME = 'STDEVs.txt'

    def __init__(self, script_path, input_path, input_filename):
        self.script_path = script_path
        self.input_path = input_path
        self.input_filename = input_filename
        self.filename_path = input_path + "/" + input_filename


    def get_thresholds_array(self):
        stds = self._calculate_stds_pandas()
        if self.COMPARE:
            self._compare_with_manual_std(stds)
        thresholds_array = self._calculate_error_thresholds(stds)

        if self.RECORD:
            self._save_results(stds, thresholds_array)
        else:
            self._compare_results(stds, thresholds_array)
        return thresholds_array

    #
    # Compare the stds obtained by pandas against the stds calculated manually.
    #
    def _compare_with_manual_std(self, stds):
        manual_stds = CalculateSTDManual.calculate_stds(self.input_path, self.input_filename)
        assert(len(stds) == len(manual_stds))

        diff = []
        for index in range(len(stds)):
            value, value_manual  = stds[index], manual_stds[index]
            if value == PandasTools.NO_DATA:
                assert(value == value_manual)  # both values must be equal to PandasTools.NO_DATA
                diff.append(value)
            else:
                diff.append(value - value_manual)

        minimum = min([10 if value == PandasTools.NO_DATA else value for value in diff])
        assert(abs(minimum) < pow(10, -10))


    def _calculate_stds_pandas(self):
        df = pd.read_csv(self.filename_path, skiprows=3, na_values=PandasTools.NO_DATA)  # skip first 3 rows (header)
        #
        # About STDEVP:
        # https://stackoverflow.com/a/14894143/4547232
        # https://stackoverflow.com/a/52642277/4547232
        #
        df_stds = df.std(ddof=0)
        stds = list(df_stds)
        stds = [PandasTools.NO_DATA if math.isnan(value) else value for value in stds]
        return stds

    @staticmethod
    def _calculate_error_thresholds(stds, param_e_list=ExperimentsUtils.THRESHOLDS):
        percentages = [param / 100 for param in param_e_list] # [0.0, 0.01, 0.03, 0.05, 0.1, 0.15, 0.2, 0.3]

        res = []
        for index, percentage in enumerate(percentages):
            stds[0] = 0  # the error threshold for the timedelta is always 0

            values = []
            for std in stds:
                if std == PandasTools.NO_DATA:
                    values.append(PandasTools.NO_DATA)
                else:
                    value = int(round(std * percentage, 0))
                    values.append(value)
            res.append({'percentage': param_e_list[index], 'values': values})
        return res

    def _save_results(self, stds, thresholds_array):
        writer = TextFileWriter(self.script_path, self.STDS_FILENAME, "a")  # "a" = append mode
        writer.write_line(self.input_filename)  # vwc_1202.dat.csv
        writer.write_line(json.dumps(stds)) # [0, 15.067395786326722, ... , 10.242778426186861]
        writer.write_line(json.dumps(thresholds_array)) # [{"percentage": 0.0, "values": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, ... , {"percentage": 0.3, "values": [0, 5, 6, 3, 4, 2, 3, 3, 2, 7, 3]}]
        writer.write_line('')
        writer.close()

    def _compare_results(self, stds, thresholds_array):
        reader = TextFileReader(self.script_path, self.STDS_FILENAME)
        while reader.continue_reading:
            if self.input_filename not in reader.read_line():
                continue
            self._compare_struct(reader.read_line(), stds)
            self._compare_struct(reader.read_line(), thresholds_array)
            return
        raise Exception("ERROR: invalid filename: " + self.input_filename)

    def _compare_struct(self, read_struct, calculated_struct):
        read_struct = json.loads(read_struct)
        if read_struct == calculated_struct:
            return
        print(self.input_filename)
        print("read_struct")
        print(read_struct)
        print("calculated_struct")
        print(calculated_struct)
        assert(read_struct == calculated_struct)




import sys
sys.path.append('.')


class ResultsConstants(object):
    #
    # These 2 csv files contain all the results returned by the compress.py script
    #
    RAW_RESULTS_PATH = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-13/2-complete"
    RAW_MM_0_FILENAME = "complete-mask-mode=0.csv"
    RAW_MM_3_FILENAME = "complete-mask-mode=3.csv"

    #
    # This csv file contains the results for MM=3 but ignoring the coders which are not present when MM=0
    # (the rows in this file match the rows in RAW_MM_0_FILENAME)
    #
    COMPARE_RESULTS_PATH = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-13/3-0vs3"
    COMPARE_MM_3_FILENAME = "complete-mask-mode=3-remove.csv"

    #
    # These 2 csv files contain all the results returned by the compress.py script merged in a single file for
    # each dataset
    #
    GLOBAL_RESULTS_PATH = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-18/3-global"
    GLOBAL_MM_0_FILENAME = "complete-mask-mode=0-global.csv"
    GLOBAL_MM_3_FILENAME = "complete-mask-mode=3-global.csv"

    @staticmethod
    def get_path_and_filename(file_key, file_value):
        ResultsConstants.check_input(file_key, file_value)

        path, filename = None, None
        if file_key == 'raw':
            path = ResultsConstants.RAW_RESULTS_PATH
            filename = ResultsConstants.RAW_MM_0_FILENAME if file_value == 0 else ResultsConstants.RAW_MM_3_FILENAME
        elif file_key == 'compare':
            path = ResultsConstants.COMPARE_RESULTS_PATH
            if file_value != 3:
                ResultsConstants.raise_error(file_key, file_value)
            filename = ResultsConstants.COMPARE_MM_3_FILENAME
        elif file_key == 'global':
            path = ResultsConstants.GLOBAL_RESULTS_PATH
            filename = ResultsConstants.GLOBAL_MM_0_FILENAME if file_value == 0 else ResultsConstants.GLOBAL_MM_3_FILENAME
        return path, filename

    @staticmethod
    def check_input(file_key, file_value):
        if file_key not in ['raw', 'compare', 'global']:
            ResultsConstants.raise_error(file_key, file_value)
        if file_value not in [0, 3]:
            ResultsConstants.raise_error(file_key, file_value)

    @staticmethod
    def raise_error(file_key, file_value):
        print "file_key = " + str(file_key)
        print "file_value = " + str(file_value)
        raise(StandardError, "ERROR: invalid combination of parameters")

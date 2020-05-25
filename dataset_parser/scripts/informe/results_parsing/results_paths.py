import sys
sys.path.append('.')


class ResultsPaths(object):
    #
    # These 2 csv files contain all the results returned by the compress_script.py script
    #
    RAW_RESULTS_PATH = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-13/2-complete"
    RAW_MM_0_FILENAME = "complete-mask-mode=0.csv"
    RAW_MM_3_FILENAME = "complete-mask-mode=3.csv"

    # These 2 csv files contain all the results returned by the compress_script.py script merged in a single file for
    # each dataset
    #
    GLOBAL_RESULTS_PATH = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-18/3-global"
    GLOBAL_MM_0_FILENAME = "complete-mask-mode=0-global.csv"
    GLOBAL_MM_3_FILENAME = "complete-mask-mode=3-global.csv"

    @staticmethod
    def get_path_and_filename(file_key, file_value):
        ResultsPaths.check_input(file_key, file_value)
        path, filename = None, None
        if file_key == 'raw':
            path = ResultsPaths.RAW_RESULTS_PATH
            if file_value == 0:
                filename = ResultsPaths.RAW_MM_0_FILENAME
            else:
                filename = ResultsPaths.RAW_MM_3_FILENAME
        elif file_key == 'global':
            path = ResultsPaths.GLOBAL_RESULTS_PATH
            if file_value == 0:
                filename = ResultsPaths.GLOBAL_MM_0_FILENAME
            else:
                filename = ResultsPaths.GLOBAL_MM_3_FILENAME

        return path, filename

    @staticmethod
    def check_input(file_key, file_value):
        if file_key in ['raw', 'global'] and file_value in [0, 3]:
            return
        print("file_key = " + str(file_key))
        print("file_value = " + str(file_value))
        raise(ValueError, "ERROR: invalid parameters")

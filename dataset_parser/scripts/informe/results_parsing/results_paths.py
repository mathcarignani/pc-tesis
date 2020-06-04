import sys
sys.path.append('.')


class ResultsPaths(object):
    PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/results/3.1/06.2020/"
    #
    # These 2 csv files contain all the results returned by the compress_script.py script
    #
    LOCAL_RESULTS_PATH = PATH + "3-local"
    LOCAL_MM_0_FILENAME = "results-mm0-local.csv"
    LOCAL_MM_3_FILENAME = "results-mm3-local.csv"

    #
    # These 2 csv files are created after running the GlobalizeResults scripts on the previous two files
    #
    GLOBAL_RESULTS_PATH = PATH + "4-global"
    GLOBAL_MM_0_FILENAME = "results-mm0-global.csv"  # GlobalizeResults(0).run()
    GLOBAL_MM_3_FILENAME = "results-mm3-global.csv"  # GlobalizeResults(3).run()

    @staticmethod
    def get_path_and_filename(mode, mask_mode):
        ResultsPaths.check_input(mode, mask_mode)
        if mode == 'local':
            path = ResultsPaths.LOCAL_RESULTS_PATH
            if mask_mode == 0:
                filename = ResultsPaths.LOCAL_MM_0_FILENAME
            else:
                filename = ResultsPaths.LOCAL_MM_3_FILENAME
        else: # mode == 'global':
            path = ResultsPaths.GLOBAL_RESULTS_PATH
            if mask_mode == 0:
                filename = ResultsPaths.GLOBAL_MM_0_FILENAME
            else:
                filename = ResultsPaths.GLOBAL_MM_3_FILENAME

        return path, filename

    @staticmethod
    def check_input(mode, mask_mode):
        if mode in ['local', 'global'] and mask_mode in [0, 3]:
            return
        print("mode = " + str(mode))
        print("mask_mode = " + str(mask_mode))
        raise(ValueError, "ERROR: invalid parameters")

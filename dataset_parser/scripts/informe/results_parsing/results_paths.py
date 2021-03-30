import sys
sys.path.append('.')


class ResultsPaths(object):
    ROOT_PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis"
    INFORME_PATH = ROOT_PATH + "/dataset_parser/scripts/informe"
    PATH = INFORME_PATH + "/results/03.2021/time-delta/3.1/"
    #
    # These 2 csv files contain all the results returned by the compress_script.py script
    #
    LOCAL_RESULTS_PATH = PATH + "1-local"
    LOCAL_FILENAME_NM = "results_NM.csv"
    LOCAL_FILENAME_M = "results_M.csv"

    #
    # These 2 csv files are created after running the GlobalizeResults scripts on the previous two files
    #
    GLOBAL_RESULTS_PATH = PATH + "2-global"
    GLOBAL_FILENAME_NM = "results_NM-global.csv"  # GlobalizeResults("NM").run()
    GLOBAL_FILENAME_M = "results_M-global.csv"  # GlobalizeResults("M").run()

    @staticmethod
    def get_path_and_filename(mode, mask_mode):
        ResultsPaths.check_input(mode, mask_mode)
        if mode == 'local':
            path = ResultsPaths.LOCAL_RESULTS_PATH
            filename = ResultsPaths.LOCAL_FILENAME_NM if mask_mode == "NM" else ResultsPaths.LOCAL_FILENAME_M
        else: # mode == 'global':
            path = ResultsPaths.GLOBAL_RESULTS_PATH
            filename = ResultsPaths.GLOBAL_FILENAME_NM if mask_mode == "NM" else ResultsPaths.GLOBAL_FILENAME_M

        return path, filename

    @staticmethod
    def check_input(mode, mask_mode):
        if mode in ['local', 'global'] and mask_mode in ["NM", "M"]:
            return
        print("mode = " + str(mode))
        print("mask_mode = " + str(mask_mode))
        raise ValueError('ERROR: invalid parameters')

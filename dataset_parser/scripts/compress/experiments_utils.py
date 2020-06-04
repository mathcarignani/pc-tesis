import sys
sys.path.append('.')

from auxi.os_utils import OSUtils
from scripts.utils import csv_files_filenames


class ExperimentsUtils(object):
    #
    # IMPORTANT: MASK_MODE should have the same value that the MASK_MODE macro used in the C++ code.
    #
    # TODO: pass MASK_MODE as a variable
    #
    MASK_MODE = 3 # 3

    CODERS = ['CoderBase', 'CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt',
              'CoderFR', 'CoderSF', 'CoderGAMPS', 'CoderGAMPSLimit']
    # TODO: remove the ALGORITHMS list
    ALGORITHMS = ["CoderPCA", "CoderAPCA", "CoderCA", "CoderPWLH", "CoderPWLHInt", "CoderGAMPSLimit"]
    CODERS_ONLY_MASK_MODE = ['CoderFR', 'CoderSF']
    THRESHOLDS = [0, 1, 3, 5, 10, 15, 20, 30]
    WINDOWS = [4, 8, 16, 32, 64, 128, 256]

    MAX_COLUMN_TYPES = 7  # ElNino

    DATASETS_ARRAY = [
        {'name': 'IRKIS', 'folder': "[1]irkis", 'o_folder': "[1]irkis", 'cols': 1},
        {'name': 'NOAA-SST', 'short_name': 'SST', 'folder': "[2]noaa-sst/months/2017", 'o_folder': "[2]noaa-sst", 'cols': 1},
        {'name': 'NOAA-ADCP', 'short_name': 'ADCP', 'folder': "[3]noaa-adcp/2015", 'o_folder': "[3]noaa-adcp", 'cols': 1},
        {'name': 'SolarAnywhere', 'short_name': 'Solar', 'folder': "[4]solar-anywhere/all", 'o_folder': "[4]solar-anywhere", 'cols': 3},
        {'name': 'ElNino', 'folder': "[5]el-nino", 'o_folder': "[5]el-nino", 'cols': 7},
        {'name': 'NOAA-SPC-hail', 'short_name': 'Hail', 'folder': "[6]noaa-spc-reports/hail", 'o_folder': "[6]noaa-spc-reports", 'cols': 3},
        {'name': 'NOAA-SPC-tornado',  'short_name': 'Tornado', 'folder': "[6]noaa-spc-reports/tornado", 'o_folder': "[6]noaa-spc-reports", 'cols': 2},
        {'name': 'NOAA-SPC-wind',  'short_name': 'Wind', 'folder': "[6]noaa-spc-reports/wind", 'o_folder': "[6]noaa-spc-reports", 'cols': 3}
    ]

    COLUMN_INDEXES = {
        'IRKIS': ['VWC'],
        'NOAA-SST': ['SST'],
        'NOAA-ADCP': ['Vel'],
        'SolarAnywhere': ['GHI', 'DNI', 'DHI'],
        'ElNino': ['Lat', 'Long', 'Z. Wind', 'M. Wind', 'Humidity', 'AirTemp', 'SST'],
        'NOAA-SPC-hail': ['Lat', 'Long', 'Size'],
        'NOAA-SPC-tornado': ['Lat', 'Long'],
        'NOAA-SPC-wind': ['Lat', 'Long', 'Speed']
    }

    DATASET_NAMES = [obj['name'] for obj in DATASETS_ARRAY]

    # DATASET_ARRAY = [
    #     {'name': 'CO2', 'folder': "CO2", 'logger': "CO2.log", 'o_folder': "CO2"},
    #     {'name': 'Humidity', 'folder': "Humidity", 'logger': "Humidity.log", 'o_folder': "Humidity"},
    #     {'name': 'Lysimeter', 'folder': "Lysimeter", 'logger': "Lysimeter.log", 'o_folder': "Lysimeter"},
    #     {'name': 'Moisture', 'folder': "Moisture", 'logger': "Moisture.log", 'o_folder': "Moisture"},
    #     {'name': 'Pressure', 'folder': "Pressure", 'logger': "Pressure.log", 'o_folder': "Pressure"},
    #     {'name': 'Radiation', 'folder': "Radiation", 'logger': "Radiation.log", 'o_folder': "Radiation"},
    #     {'name': 'Snow_height', 'folder': "Snow_height", 'logger': "Snow_height.log", 'o_folder': "Snow_height"},
    #     {'name': 'Temperature', 'folder': "Temperature", 'logger': "Temperature.log", 'o_folder': "Temperature"},
    #     {'name': 'Voltage', 'folder': "Voltage", 'logger': "Voltage.log", 'o_folder': "Voltage"},
    #     {'name': 'Wind_direction', 'folder': "Wind_direction", 'logger': "Wind_direction.log", 'o_folder': "Wind_direction"},
    #     {'name': 'Wind_speed', 'folder': "Wind_speed", 'logger': "Wind_speed.log", 'o_folder': "Wind_speed"},
    # ]

    @staticmethod
    def expected_coders(mask_mode):
        if mask_mode == 0:
            return [item for item in ExperimentsUtils.CODERS if item not in ExperimentsUtils.CODERS_ONLY_MASK_MODE]
        else:
            return ExperimentsUtils.CODERS

    @staticmethod
    def dataset_csv_filenames(dataset_name):
        input_path = ExperimentsUtils.CSV_PATH + ExperimentsUtils.get_dataset_info(dataset_name)['folder']
        filenames = csv_files_filenames(input_path)
        if dataset_name in ["NOAA-SST", "NOAA-ADCP"]:
            filenames = filenames[:3]  # only consider the first three files for these datasets
        return filenames

    @staticmethod
    def datasets_with_multiple_files():
        result = []
        for name in ExperimentsUtils.DATASET_NAMES:
            if ExperimentsUtils.dataset_csv_files_count(name) > 1:
                result.append(name)
        return result

    @staticmethod
    def dataset_csv_files_count(dataset_name):
        return len(ExperimentsUtils.dataset_csv_filenames(dataset_name))

    @staticmethod
    def get_dataset_info(dataset_name):
        for dataset in ExperimentsUtils.DATASETS_ARRAY:
            if dataset['name'] == dataset_name:
                return dataset
        raise(KeyError, "Invalid dataset_name: " + dataset_name)

    @staticmethod
    def get_dataset_data_columns_count(dataset_name):
        return ExperimentsUtils.get_dataset_info(dataset_name)['cols']

    @staticmethod
    def get_dataset_path(dataset_name):
        return ExperimentsUtils.CSV_PATH + ExperimentsUtils.get_dataset_info(dataset_name)['folder']

    @staticmethod
    def get_dataset_short_name(dataset_name):
        dataset_info = ExperimentsUtils.get_dataset_info(dataset_name)
        return dataset_info.get('short_name') or dataset_info.get('name')

    CSV_PATH = OSUtils.datasets_csv_path()

    CODERS_ARRAY = [
        {
            'name': 'CoderBase',
            'o_folder': 'base'
        },
        {
            'name': 'CoderPCA',
            'o_folder': 'pca',
            'params': {'window_size': WINDOWS}
        },
        {
            'name': 'CoderAPCA',
            'o_folder': 'apca',
            'params': {'window_size': WINDOWS}
        },
        {
            'name': 'CoderCA',
            'o_folder': 'ca',
            'params': {'window_size': WINDOWS}
        },
        {
            'name': 'CoderPWLH',
            'o_folder': 'pwlh',
            'params': {'window_size': WINDOWS}
        },
        {
            'name': 'CoderPWLHInt',
            'o_folder': 'pwlh-int',
            'params': {'window_size': WINDOWS}
        },
        {
            'name': 'CoderGAMPS',
            'o_folder': 'gamps',
            'params': {'window_size': WINDOWS}
        },
        {
            'name': 'CoderGAMPSLimit',
            'o_folder': 'gamps-limit',
            'params': {'window_size': WINDOWS}
        },
    ]

    MASK_MODE_CODERS_ARRAY = [
        {
            'name': 'CoderFR',
            'o_folder': 'fr',
            'params': {'window_size': WINDOWS}
        },
        {
            'name': 'CoderSF',
            'o_folder': 'sf',
            'params': {'window_size': [4]}  # window_size param doesn't matter
        }
    ]

    if MASK_MODE > 0:
        CODERS_ARRAY += MASK_MODE_CODERS_ARRAY

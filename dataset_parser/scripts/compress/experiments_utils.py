import sys
sys.path.append('.')

from auxi.os_utils import datasets_csv_path
from scripts.utils import csv_files_filenames


class ExperimentsUtils(object):
    CODERS = ['CoderBasic', 'CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt',
              'CoderFR', 'CoderSF', 'CoderGAMPS', 'CoderGAMPSLimit']
    ALGORITHMS = ["CoderPCA", "CoderAPCA", "CoderCA", "CoderPWLH", "CoderPWLHInt", "CoderGAMPSLimit"]
    CODERS_ONLY_MASK_MODE = ['CoderFR', 'CoderSF']
    CODERS_NO_MASK_MODE = [item for item in CODERS if item not in CODERS_ONLY_MASK_MODE]
    THRESHOLDS = [0, 1, 3, 5, 10, 15, 20, 30]
    WINDOWS = [4, 8, 16, 32, 64, 128, 256]

    MAX_COLUMN_TYPES = 7  # ElNino

    DATASETS_ARRAY = [
        {'name': 'IRKIS', 'folder': "[1]irkis", 'logger': "irkis.log", 'o_folder': "[1]irkis", 'cols': 1},
        {'name': 'NOAA-SST', 'folder': "[2]noaa-sst/months/2017", 'logger': "noaa-sst.log", 'o_folder': "[2]noaa-sst", 'cols': 1},
        {'name': 'NOAA-ADCP', 'folder': "[3]noaa-adcp/2015", 'logger': "noaa-adcp.log", 'o_folder': "[3]noaa-adcp", 'cols': 1},
        {'name': 'SolarAnywhere', 'folder': "[4]solar-anywhere/all", 'logger': "solar-anywhere.log", 'o_folder': "[4]solar-anywhere", 'cols': 3},
        {'name': 'ElNino', 'folder': "[5]el-nino", 'logger': "el-nino.log", 'o_folder': "[5]el-nino", 'cols': 7},
        {'name': 'NOAA-SPC-hail', 'folder': "[6]noaa-spc-reports/hail", 'logger': "noaa-spc-hail.log", 'o_folder': "[6]noaa-spc-reports", 'cols': 3},
        {'name': 'NOAA-SPC-tornado', 'folder': "[6]noaa-spc-reports/tornado", 'logger': "noaa-spc-tornado.log", 'o_folder': "[6]noaa-spc-reports", 'cols': 2},
        {'name': 'NOAA-SPC-wind', 'folder': "[6]noaa-spc-reports/wind", 'logger': "noaa-spc-wind.log", 'o_folder': "[6]noaa-spc-reports", 'cols': 3}
    ]

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
    def dataset_csv_filenames(dataset_name):
        input_path = ExperimentsUtils.CSV_PATH + ExperimentsUtils.get_dataset_info(dataset_name)['folder']
        filenames = csv_files_filenames(input_path)
        if dataset_name in ["NOAA-SST", "NOAA-ADCP"]:
            filenames = filenames[:3]  # only consider the first three files for these datasets
        return filenames

    @staticmethod
    def get_dataset_info(dataset_name):
        for dataset in ExperimentsUtils.DATASETS_ARRAY:
            if dataset['name'] == dataset_name:
                return dataset
        print dataset_name
        raise StandardError

    @staticmethod
    def get_dataset_data_columns_count(dataset_name):
        return ExperimentsUtils.get_dataset_info(dataset_name)['cols']

    CSV_PATH = datasets_csv_path()

    MASK_MODE = False

    CODERS_ARRAY = [
        {
            'name': 'CoderBasic',
            'o_folder': 'basic'
        },
        # {
        #     'name': 'CoderPCA',
        #     'o_folder': 'pca',
        #     'params': {'window_size': ExperimentsUtils.WINDOWS}
        # },
        # {
        #     'name': 'CoderAPCA',
        #     'o_folder': 'apca',
        #     'params': {'window_size': ExperimentsUtils.WINDOWS}
        # },
        # {
        #     'name': 'CoderCA',
        #     'o_folder': 'ca',
        #     'params': {'window_size': ExperimentsUtils.WINDOWS}
        # },
        # {
        #     'name': 'CoderPWLH',
        #     'o_folder': 'pwlh',
        #     'params': {'window_size': ExperimentsUtils.WINDOWS}
        # },
        # {
        #     'name': 'CoderPWLHInt',
        #     'o_folder': 'pwlh-int',
        #     'params': {'window_size': ExperimentsUtils.WINDOWS}
        # },
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
        # {
        #     'name': 'CoderFR',
        #     'o_folder': 'fr',
        #     'params': {'window_size': ExperimentsUtils.WINDOWS}
        # },
        # {
        #     'name': 'CoderSF',
        #     'o_folder': , 'sf',
        #     'params': {'window_size': [4]}  # window_size param doesn't matter
        # }
    ]

    if MASK_MODE:
        CODERS_ARRAY += MASK_MODE_CODERS_ARRAY

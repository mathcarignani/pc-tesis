
from auxi.os_utils import datasets_csv_path


THRESHOLD_PERCENTAGES = [0, 1, 3, 5, 10, 15, 20, 30]
WINDOW_SIZES = [4, 8, 16, 32, 64, 128, 256]

CSV_PATH = datasets_csv_path()
MASK_MODE = False


#
# Returns true iff the file muset be skiped
#
def skip_file(dataset_name, file_index):
    return dataset_name in ["NOAA-SST", "NOAA-ADCP"] and file_index >= 3


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

CODERS_ARRAY = [
    {
        'name': 'CoderBasic',
        'o_folder': 'basic'
    },
    # {
    #     'name': 'CoderPCA',
    #     'o_folder': 'pca',
    #     'params': {'window_size': WINDOW_SIZES}
    # },
    # {
    #     'name': 'CoderAPCA',
    #     'o_folder': 'apca',
    #     'params': {'window_size': WINDOW_SIZES}
    # },
    # {
    #     'name': 'CoderCA',
    #     'o_folder': 'ca',
    #     'params': {'window_size': WINDOW_SIZES}
    # },
    # {
    #     'name': 'CoderPWLH',
    #     'o_folder': 'pwlh',
    #     'params': {'window_size': WINDOW_SIZES}
    # },
    # {
    #     'name': 'CoderPWLHInt',
    #     'o_folder': 'pwlh-int',
    #     'params': {'window_size': WINDOW_SIZES}
    # },
    {
        'name': 'CoderGAMPS',
        'o_folder': 'gamps',
        'params': {'window_size': WINDOW_SIZES}
    },
    {
        'name': 'CoderGAMPSLimit',
        'o_folder': 'gamps-limit',
        'params': {'window_size': WINDOW_SIZES}
    },
]

MASK_MODE_CODERS_ARRAY = [
    # {
    #     'name': 'CoderFR',
    #     'o_folder': 'fr',
    #     'params': {'window_size': WINDOW_SIZES}
    # },
    # {
    #     'name': 'CoderSF',
    #     'o_folder': , 'sf',
    #     'params': {'window_size': [4]}  # window_size param doesn't matter
    # }
]

if MASK_MODE:
    CODERS_ARRAY += MASK_MODE_CODERS_ARRAY

import sys
sys.path.append('.')


from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.latex_tables.table_datasets.latex_table import LatexTable
from scripts.informe.latex_tables.table_datasets.pandas_analysis import PandasAnalysis


class TableDatasets(object):
    @staticmethod
    def generate_table_irkis():
        filenames, path = TableDatasets.get_filenames_and_path('IRKIS')
        assert(len(filenames) == 7)
        table = LatexTable('1-IRKIS-stats.tex')

        for filename in filenames: # filenames[0:1]:
            data = TableDatasets.get_data(path, filename)
            pos1, pos2 = filename.find('_'), filename.find('.') # vwc_SLF2.smet.csv
            station = filename[pos1+1:pos2] # SLF2
            data['name'] = station
            table.add_data_irkis(data)

    @staticmethod
    def generate_table_sst():
        filenames, path = TableDatasets.get_filenames_and_path('NOAA-SST')
        assert(len(filenames) == 3)
        table = LatexTable('2-SST-stats.tex')

        for idx, filename in enumerate(filenames):
            data = TableDatasets.get_data(path, filename)
            data['name'] = '0' + str(idx + 1) + '-2017'
            table.add_data_sst(data)

    @staticmethod
    def generate_table_adcp():
        filenames, path = TableDatasets.get_filenames_and_path('NOAA-ADCP')
        assert(len(filenames) == 3)
        table = LatexTable('3-ADCP-stats.tex')

        for idx, filename in enumerate(filenames):
            data = TableDatasets.get_data(path, filename)
            data['name'] = '0' + str(idx + 1) + '-2015'
            table.add_data_adcp(data)

    @staticmethod
    def generate_table_elnino():
        filenames, path = TableDatasets.get_filenames_and_path('ElNino')
        assert(len(filenames) == 1)
        filename = filenames[0]
        table = LatexTable('5-ElNino-stats.tex')

        column_names = ExperimentsUtils.COLUMN_INDEXES['ElNino']
        data_array = TableDatasets.get_data(path, filename, len(column_names))
        for idx, column in enumerate(column_names):
            data = data_array[idx]
            data['name'] = column_names[idx]
            table.add_data_elnino(data)

    @staticmethod
    def get_data(path, filename, columns_length=None):
        file_path = path + '/' + filename
        return PandasAnalysis.get_data(file_path, columns_length)

    @staticmethod
    def get_filenames_and_path(dataset):
        filenames = ExperimentsUtils.dataset_csv_filenames(dataset)
        path = ExperimentsUtils.get_dataset_path(dataset)
        return filenames, path


# TableDatasets.generate_table_irkis()
# TableDatasets.generate_table_sst()
# TableDatasets.generate_table_adcp()
TableDatasets.generate_table_elnino()



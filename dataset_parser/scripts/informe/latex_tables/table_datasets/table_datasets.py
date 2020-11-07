import sys
sys.path.append('.')


from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.latex_tables.table_datasets.latex_table import LatexTable
from scripts.informe.latex_tables.table_datasets.pandas_analysis import PandasAnalysis

# TODO: move to the latex_tables path
class TableDatasets(object):
    @staticmethod
    def generate_table_irkis():
        dataset = 'IRKIS'
        filenames = ExperimentsUtils.dataset_csv_filenames(dataset)
        path = ExperimentsUtils.get_dataset_path(dataset)

        table = LatexTable('1-IRKIS-stats.tex')

        for filename in filenames: # filenames[0:1]:
            file_path = path + '/' + filename
            data = PandasAnalysis.get_data(file_path)

            pos1, pos2 = filename.find('_'), filename.find('.') # vwc_SLF2.smet.csv
            station = filename[pos1+1:pos2] # SLF2

            data['name'] = station
            table.add_data_irkis(data)


TableDatasets.generate_table_irkis()

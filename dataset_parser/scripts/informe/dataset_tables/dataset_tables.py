import sys
sys.path.append('.')



from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.dataset_tables.latex_table import LatexTable
from scripts.informe.dataset_tables.pandas_analysis import PandasAnalysis

class DatasetAnalysis(object):



    @staticmethod
    def generate_table_irkis():
        dataset = 'IRKIS'
        filenames = ExperimentsUtils.dataset_csv_filenames(dataset)
        path = ExperimentsUtils.get_dataset_path(dataset)

        table = LatexTable('IRKIS.txt')

        for filename in filenames: # filenames[0:1]:
            file_path = path + '/' + filename
            data = PandasAnalysis.get_data(file_path)

            pos1, pos2 = filename.find('_'), filename.find('.') # vwc_SLF2.smet.csv
            station = filename[pos1+1:pos2] # SLF2

            data['name'] = station
            table.add_data(data)


DatasetAnalysis.generate_table_irkis()
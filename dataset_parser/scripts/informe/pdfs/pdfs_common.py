import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages
from scripts.compress.experiments_utils import ExperimentsUtils


class PDFSCommon(object):
    def __init__(self, path, global_mode, datasets_names=None):
        self.path = path
        self.global_mode = global_mode
        self.dataset_names = datasets_names or ExperimentsUtils.DATASET_NAMES

        # iteration variables
        self.dataset_id = None
        self.dataset_name = None
        self.filename = None
        self.pdf = None
        self.pdf_name = None

    def create_pdfs(self):
        for dataset_id, self.dataset_name in enumerate(self.dataset_names):
            print(self.dataset_name)
            self.dataset_id = dataset_id + 1
            self.created_dataset_pdf_file()

    def created_dataset_pdf_file(self):
        self.pdf_name = self.path + str(self.dataset_id) + "-" + self.dataset_name + ".pdf"
        with PdfPages(self.pdf_name) as self.pdf:
            for self.filename in self.dataset_filenames():
                print("  " + self.filename)
                self.create_pdf_pages(self.pdf, self.dataset_name, self.filename)

    def dataset_filenames(self):
        filenames = ExperimentsUtils.dataset_csv_filenames(self.dataset_name)
        filenames = ['Global'] if self.global_mode and len(filenames) > 1 else filenames
        return filenames

    @staticmethod
    def column_indexes(dataset_name):
        return range(1, ExperimentsUtils.get_dataset_data_columns_count(dataset_name) + 1)

import sys
sys.path.append('.')

from scripts.informe.pdfs.pdfs1 import PDFS1
# from scripts.informe.pdfs.pdfs2 import PDFS2
from scripts.informe.pdfs.pdfs3 import PDFS3
from scripts.informe.pdfs.pdfs4 import PDFS4
from scripts.informe.data_analysis.process_results.process_results import ProcessResults
from scripts.compress.compress_script import CompressScript
from scripts.compress.globalize.globalize_results import GlobalizeResults
from scripts.informe.gzip_compare.gzip_script import GZipScript

# TO RUN SCRIPT:
# - Install Python 3.7.0
# - Run "pip install -r requirements.txt"
# - Run "python scripts/informe/results/run.py"

class Run:
    ROOT_PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis"
    INFORME_PATH = ROOT_PATH + "/dataset_parser/scripts/informe"
    RESULTS_PATH = INFORME_PATH + "/results/03.2021/"

    @classmethod
    def compress_script(cls):
        CompressScript("results_NM.csv", "NM").run()
        # CompressScript("results_M.csv", "M").run()

    @classmethod
    def globalize_results(cls):
        GlobalizeResults("NM").run()
        GlobalizeResults("M").run()

    @classmethod
    def relative_performance(cls):
        pdf1_path = Run.RESULTS_PATH + '3.2/'
        pdf1 = PDFS1(pdf1_path, 'global')
        pdf1.create_pdfs()
        pdf1.create_latex_table(pdf1_path)

    @classmethod
    def window_parameter(cls):
        pdf3_path = Run.RESULTS_PATH + '3.3/'
        pdf3 = PDFS3(pdf3_path + 'window/')
        pdf3.create_pdfs()  # LOCAL (BEST LOCAL WINDOW VS. BEST GLOBAL WINDOW)
        pdf3.create_latex_table(pdf3_path)

    @classmethod
    def mask_coders(cls):
        pdf4_path = Run.RESULTS_PATH + '3.4/'
        PDFS4(pdf4_path + 'pdf/', 'global').create_pdfs()  # GLOBAL
        ProcessResults(True, pdf4_path + 'results1', 1).run()

    @classmethod
    def mask_coders_and_gzip(cls):
        pdf4_path = Run.RESULTS_PATH + '3.4/'
        gzip_path = pdf4_path + 'gzip/'
        # GZipScript(gzip_path, 'results.csv', False).run()
        # GZipScript(gzip_path, 'results-t.csv', True).run()
        ProcessResults(True, pdf4_path + 'results2', 2, gzip_path, 'results-t.csv').run()

# (0) Run "sh make_mac.sh" / "sh make_ubuntu.sh" so that the following executables are created:
# run_variant_NM
# run_variant_M

# (3.1) Experimental Setting
#
# (1) Run the compress script for each mode, each execution creates a different results csv file
# Run.compress_script()

# (2) Globalize the result files generated in step (1)
# Run.globalize_results()

# (3.2) Relative Performance of the Coders
# Run.relative_performance()

# (3.3) Window Size Parameter
# Run.window_parameter()


# (3.4) Mask Coders Performance
# Run.mask_coders()
Run.mask_coders_and_gzip()




import sys
sys.path.append('.')

from scripts.informe.pdfs.pdfs1 import PDFS1
from scripts.informe.pdfs.pdfs2 import PDFS2
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


# TODO: define mode paths
ROOT_PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis"
INFORME_PATH = ROOT_PATH + "/dataset_parser/scripts/informe"
RESULTS_PATH = INFORME_PATH + "/results/10.2020/"

#
# (0) Run "sh make_mac.sh" / "sh make_ubuntu.sh" so that the following executables are created:
# run_variant_NM
# run_variant_M
#

#
# (3.1) Experimental Setting
#
# (1) Run the compress script for each mode, each execution creates a different results csv file
# CompressScript("results_NM.csv", "NM").run()
# CompressScript("results_M.csv", "M").run()

#
# (2) Globalize the result files generated in step (1)
# GlobalizeResults("NM").run()
# GlobalizeResults("M").run()


#
# (3.2) Relative Performance of the Coders
#
pdf1 = PDFS1(RESULTS_PATH + '3.2/', 'global')
pdf1.create_pdfs()
pdf1.create_latex_table(RESULTS_PATH + '3.2/')


# #
# # 3.3 Window Size Parameter
# #
# PDFS3(RESULTS_PATH + '3.3/window/').create_pdfs()  # LOCAL (BEST LOCAL WINDOW VS. BEST GLOBAL WINDOW)


# #
# # 3.4 Mask Coders Performance
# #
# PDFS4(RESULTS_PATH + '3.4/pdf/', 'global').create_pdfs()  # GLOBAL
# ProcessResults(True, RESULTS_PATH + '3.4/results1', 1).run()

# gzip_path = RESULTS_PATH + '3.4/gzip/'
# GZipScript(gzip_path, 'results.csv', False).run()
# GZipScript(gzip_path, 'results-t.csv', True).run()
# ProcessResults(True, RESULTS_PATH + '3.4/results2', 2, gzip_path, 'results-t.csv').run()

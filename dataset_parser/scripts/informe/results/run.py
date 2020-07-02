import sys
sys.path.append('.')

from scripts.informe.pdfs.pdfs1 import PDFS1
from scripts.informe.pdfs.pdfs2 import PDFS2
from scripts.informe.pdfs.pdfs3 import PDFS3
from scripts.informe.pdfs.pdfs4 import PDFS4
from scripts.informe.data_analysis.process_results.process_results import ProcessResults
from scripts.compress.compress_script import CompressScript
from scripts.compress.globalize.globalize_results import GlobalizeResults


# TO RUN SCRIPT:
# - Install Python 3.7.0
# - Run "pip install -r requirements.txt"
# - Run "python scripts/informe/results/run.py"


# TODO: define mode paths
PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/results/"

#
# (0) Compile the CPP code in both modes so that the following executables are created:
# cpp_project_0
# cpp_project_3
# TODO: change the name of the executables to exe_mode_0 and exe_mode_3
#

#
# (3.1) Experimental Setting
#
# (1) Run the compress script for each mode, each execution creates a different results.csv file
# CompressScript("results.csv", 0).run()
# CompressScript("results.csv", 0).run()
# TODO: make changes to pass the mode as an argument and output different modes to different folders (inside 3.1)
#
# (2) Globalize the result files generated in step (1)
# GlobalizeResults(0).run()
# GlobalizeResults(3).run()


#
# (3.2) Relative Performance of the Coders
#
# PDFS1(PATH + '3.2/', 'local').create_pdfs() # TODO: delete line
PDFS1(PATH + '3.2/', 'global').create_pdfs()


# #
# # 3.3 Window Size Parameter
# #
# # PDFS2(PATH + '3.3/', 'local).create_pdfs()  # LOCAL - TODO: delete line
# # PDFS2(PATH + '3.3/', 'global).create_pdfs()  # GLOBAL - TODO: delete line
# PDFS3(PATH + '3.3/window/').create_pdfs()  # LOCAL (BEST LOCAL WINDOW VS. BEST GLOBAL WINDOW)



# #
# # 3.4 Mask Coders Performance
# #
# PDFS4(PATH + '3.4/pdf/', 'global').create_pdfs()  # GLOBAL
ProcessResults(True, PATH + '3.4/results1', 1).run() # includes MinMax table

# TODO: delete
# # ProcessResults(True, PATH + '3.4/results12', 12).run()
# # ProcessResults(True, PATH + '3.4/results2', 2).run()
# # ProcessResults(True, PATH + '3.4/results3', 3).run()
# # ProcessResults(True, PATH + '3.4/results4', 4).run()
# ProcessResults(True, PATH + '3.4/results61', 61).run()
# ProcessResults(True, PATH + '3.4/results62', 62).run()
# ProcessResults(True, PATH + '3.4/results63', 63).run()




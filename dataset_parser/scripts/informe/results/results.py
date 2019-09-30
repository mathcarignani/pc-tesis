import sys
sys.path.append('.')

from scripts.informe.pdfs.pdfs1 import PDFS1
from scripts.informe.pdfs.pdfs2 import PDFS2
from scripts.informe.data_analysis.process_results.process_results import ProcessResults

#
# python scripts/informe/results/results.py
#
PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/results/"




#
# 3.2 Relative Performance of the Coders
#

# PDFS1(PATH + '3.2/', False).create_pdfs()
# PDFS1(PATH + '3.2/', True).create_pdfs()

#
# 3.3 Mask Coders Performance
#

ProcessResults(True, PATH + '3.3/', False).run()
ProcessResults(True, PATH + '3.3/', True).run()

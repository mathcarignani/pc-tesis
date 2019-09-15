import sys
sys.path.append('.')

from scripts.informe.pdfs.pdfs1 import PDFS1
from scripts.informe.pdfs.pdfs2 import PDFS2

#
# python scripts/informe/results/results.py
#
PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/results/"




#
# 3.2 Relative Performance of the Coders
#

PDFS1(PATH + 'pdfs1/', False).create_pdfs()
PDFS1(PATH + 'pdfs1/', True).create_pdfs()

from parser import Parser
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

class ParserVWC(Parser):
	def __init__(self):
		super(ParserVWC, self).__init__()
		self.nodata = "-999.000000"

	# In the vwc files the header is only the first line.
	# EXAMPLE:
	# timestamp -10cm_A -30cm_A -50cm_A -80cm_A -120cm_A -10cm_B -30cm_B -50cm_B -80cm_B -120cm_B
	def _parse_header(self, line):
		s_line = line.split()
		self._parse_columns(s_line)
		self.parsing_header = False

	def plot(self):
		ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
		ts = ts.cumsum()
		df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
		df = df.cumsum()
		plt.figure(); df.plot();
		plt.savefig("1.png")
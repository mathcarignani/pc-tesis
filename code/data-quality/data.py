import pandas as pd
import numpy as np

class Data:
	SUPPORTED_VERSIONS = ['1.0', '1.1']
	KELVIN_OFFSET = 273.15

	def __init__(self):
		self.version = None
		self.df = None
		self.nodata = None
		self.units_offset = None
		self.units_multiplier = None

	def set_version(self, version):
		if version not in self.SUPPORTED_VERSIONS:
			raise ValueError('Version' + version + 'not supported.')
		self.version = version

	def parse_header(self, s_line):
		if s_line[0] == 'fields':
			# EXAMPLE:
			# fields = timestamp TA RH VW VW_max DW ISWR OSWR HS TSS TS1 TS2 TS3 PSUM Ventilation U_Battery T_logger
			self.df = pd.DataFrame(columns=s_line[3:])
		elif s_line[0] == 'nodata':
			# EXAMPLE:
			# nodata = -999
			self.nodata = s_line[2]
		elif s_line[0] == 'units_offset':
			# EXAMPLE
			# units_offset     = 0 273.15 0 0 0 0 0 0 0 273.15 273.15 273.15 273.15 0 0 0 0
			self.units_offset = np.array(s_line[3:]).astype(np.float)
		elif s_line[0] == 'units_multiplier':
			# EXAMPLE
			# units_multiplier = 1 1 0.01 1 1 1 1 1 0.01 1 1 1 1 1 1 1 1
			self.units_multiplier = np.array(s_line[3:]).astype(np.float)

		return s_line[0] != '[DATA]'

	def parse_data(self, s_line):
		# EXAMPLE:
		# 2009-10-01T01:00  278.92   273.89   273.89    1.4     0    0.0      0      0 263.637  0.000    0.000   0.926
		timestamp = pd.to_datetime(s_line[0])
		if self.nodata:
			# convert strings equal to self.nodata to np.nan
			s_line = [np.nan if x is self.nodata else x for x in s_line]
		self.df.loc[timestamp] = np.array(s_line[1:]).astype(np.float)

	def post_parsing(self):
		column_names = self.df.columns.values
		if self.version == '1.0':
			self.apply_offset(column_names)
			self.apply_multiplier(column_names)
		else: # self.version == '1.1':
			self.apply_multiplier(column_names)
			self.apply_offset(column_names)

	def apply_offset(self, column_names):
		if len(self.units_offset) == len(column_names):
			for idx, col_name in enumerate(column_names):
				col_offset = self.units_offset[idx]
				if col_offset != 0:
					if col_offset == self.KELVIN_OFFSET:
						break # do not convert Celsius to Kelvin
					else:
						print col_name, self.units_offset[idx]
						self.df[col_name] += self.units_offset[idx]

	def apply_multiplier(self, column_names):
		if len(self.units_multiplier) == len(column_names):
			for idx, col_name in enumerate(column_names):
				col_mult = self.units_multiplier[idx]
				if col_mult != 1:
					self.df[col_name] *= col_mult

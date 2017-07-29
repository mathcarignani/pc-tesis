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
		self.columns_count = 0
		self.fail = {'missing_values': [], 'errors': [], 'duplicate_rows': []}
		self.last_date = None

	def set_nodata(self, nodata="-999.000000"):
		self.nodata = nodata

	def set_version(self, s_line):
		# EXAMPLE:
		# SMET 1.1 ASCII
		version = s_line[1]
		if version not in self.SUPPORTED_VERSIONS:
			raise StandardError('Version' + version + 'not supported.')
		self.version = version

	def parse_header(self, s_line):
		if s_line[0] == 'fields':
			# EXAMPLE:
			# fields = timestamp TA RH VW VW_max DW ISWR OSWR HS TSS TS1 TS2 TS3 PSUM Ventilation U_Battery T_logger
			self.parse_fields(s_line[2:])
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

		header_end = s_line[0] == '[DATA]'
		if header_end:
			self.check_valid_header()
		return not(header_end)

	def parse_fields(self, s_line):
		# EXAMPLE:
		# timestamp TA RH VW VW_max DW ISWR OSWR HS TSS TS1 TS2 TS3 PSUM Ventilation U_Battery T_logger
		self.df = pd.DataFrame(columns=s_line[1:])
		self.columns_count = len(self.df.columns)

	def check_valid_header(self):
		if not(self.nodata):
			raise StandardError('The header is missing the nodata attribute.')

	def parse_data(self, s_line, line):
		# EXAMPLE:
		# 2009-10-01T01:00  278.92   273.89   273.89    1.4     0    0.0      0      0 263.637  0.000    0.000   0.926
		try:
			timestamp = pd.to_datetime(s_line[0])
			data = s_line[1:]
			if len(data) == self.columns_count:

				current_date = s_line[0]
				if current_date == self.last_date:
					self.fail['duplicate_rows'].append(line)
				else:
					data = [np.nan if x == self.nodata else x for x in data]
					np_array = np.array(data).astype(np.float)
				self.last_date = current_date
			else:
				# if the line has an inconsistent number of values mark the whole row as invalid
				self.fail['missing_values'].append(line)
				np_array = np.array([np.nan] * len(self.df.columns))
			
			self.df.loc[timestamp] = np_array
		except:
			self.fail['errors'].append(line)

	def post_parsing(self):
		column_names = self.df.columns.values
		if self.version == '1.0':
			self.apply_offset(column_names)
			self.apply_multiplier(column_names)
		else: # self.version == '1.1':
			self.apply_multiplier(column_names)
			self.apply_offset(column_names)
		
	def apply_offset(self, column_names):
		if (self.units_offset is not None) and len(self.units_offset) == len(column_names):
			for idx, col_name in enumerate(column_names):
				col_offset = self.units_offset[idx]
				if col_offset != 0:
					if col_offset == self.KELVIN_OFFSET:
						break # do not convert Celsius to Kelvin
					else:
						print col_name, self.units_offset[idx]
						self.df[col_name] += self.units_offset[idx]

	def apply_multiplier(self, column_names):
		if (self.units_multiplier is not None) and len(self.units_multiplier) == len(column_names):
			for idx, col_name in enumerate(column_names):
				col_mult = self.units_multiplier[idx]
				if col_mult != 1:
					self.df[col_name] *= col_mult

	def analize(self):
		print "Total dataset length:", len(self.df.index)
		print "Total nan rows:", len(self.df.index[self.df.isnull().all(1)])
		print "Dataset stats:"
		print self.df.describe()
		print
		print "Null values count:"
		print self.df.isnull().sum()
		print
		print "Duplicate rows:"
		for p in self.fail['duplicate_rows']: print p
		print
		print "Invalid lines (missing values) -", len(self.fail['missing_values'])
		for p in self.fail['missing_values']: print p
		print
		print "Invalid lines (errors) -", len(self.fail['errors'])
		for p in self.fail['errors']: print p


from parser import *

class ParserSMET(Parser):
	SUPPORTED_VERSIONS = ['1.0', '1.1']
	KELVIN_OFFSET = 273.15

	def __init__(self):
		super(ParserSMET, self).__init__()
		self.nodata = None
		self.version = None
		self.units_offset = None
		self.units_multiplier = None

	def _parse_header(self, line):
		s_line = line.split()
		parsing_header = True
		if s_line[0] == 'SMET':
			# EXAMPLE:
			# SMET 1.1 ASCII
			version = s_line[1]
			if version not in self.SUPPORTED_VERSIONS:
				raise StandardError('Version' + version + 'not supported.')
			self.version = version
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
		elif s_line[0] == 'fields':
			# EXAMPLE:
			# fields = timestamp TA RH VW VW_max DW ISWR OSWR HS TSS TS1 TS2 TS3 PSUM Ventilation U_Battery T_logger
			self._parse_columns(s_line[2:])
		elif s_line[0] == '[DATA]':
			# EXAMPLE:
			# [DATA]
			parsing_header = False
		return parsing_header

	def process_data(self):
		self._post_parsing()
		super(ParserSMET, self).process_data()

	def _post_parsing(self):
		column_names = self.df.columns.values
		if self.version == '1.0':
			self._apply_offset(column_names)
			self._apply_multiplier(column_names)
		else: # self.version == '1.1':
			self._apply_multiplier(column_names)
			self._apply_offset(column_names)
		
	def _apply_offset(self, column_names):
		if (self.units_offset is not None) and len(self.units_offset) == len(column_names):
			for idx, col_name in enumerate(column_names):
				col_offset = self.units_offset[idx]
				if col_offset != 0:
					if col_offset == self.KELVIN_OFFSET:
						break # leave temperature as Celsius, do not convert to Kelvin
					else:
						# print col_name, self.units_offset[idx]
						self.df[col_name] += self.units_offset[idx]

	def _apply_multiplier(self, column_names):
		if (self.units_multiplier is not None) and len(self.units_multiplier) == len(column_names):
			for idx, col_name in enumerate(column_names):
				col_mult = self.units_multiplier[idx]
				if col_mult != 1:
					self.df[col_name] *= col_mult
#ifndef __CSV_UTILS_H__
#define __CSV_UTILS_H__

class CsvUtils {

public:

	// Code first row_count rows from csv file input_file into output_file.
	// static void code_csv_unary(int row_count, char* input_file, char* output_file);
	static void code_csv_unary();

	// Decode first row_count rows from input_file into output_file.
	static void decode_csv_unary(int row_count, char* input_file, char* output_file);

};

#endif

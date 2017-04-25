#ifndef __CSV_UTILS_H__
#define __CSV_UTILS_H__

class CsvUtils {

public:
	static void code_csv(std::string filename, std::string coded_filename);
	static void decode_csv(std::string coded_filename, std::string decoded_filename);
	static int compare_csv(std::string filename1, std::string filename2);
};

#endif

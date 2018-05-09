
#ifndef CPP_PROJECT_CSV_UTILS_H
#define CPP_PROJECT_CSV_UTILS_H

#include <string>

class CSVUtils {

public:
    static int lineCount(std::string path, std::string filename);

    static void CopyCSV(std::string path1, std::string filename1, std::string path2, std::string filename2);

    static void CompareCSVLossless(std::string path1, std::string filename1, std::string path2, std::string filename2);

};

#endif //CPP_PROJECT_CSV_UTILS_H

//
//#ifndef CPP_PROJECT_CSV_UTILS_H
//#define CPP_PROJECT_CSV_UTILS_H
//
//#include <string>
//
//class CsvUtils {
//
//public:
//    static void code_csv(std::string filename, std::string coded_filename);
//    static void decode_csv(std::string coded_filename, std::string decoded_filename);
//    static int compare_csv(std::string filename1, std::string filename2);
//};
//
//#endif //CPP_PROJECT_CSV_UTILS_H

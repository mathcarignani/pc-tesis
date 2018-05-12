
#ifndef CPP_PROJECT_CSV_UTILS_H
#define CPP_PROJECT_CSV_UTILS_H

#include <string>

class CSVUtils {

public:
    static void CopyCSV(std::string path1, std::string filename1, std::string path2, std::string filename2);

    static void CompareCSVLossless(std::string path1, std::string filename1, std::string path2, std::string filename2);

};

#endif //CPP_PROJECT_CSV_UTILS_H

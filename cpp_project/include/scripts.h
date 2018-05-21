
#ifndef CPP_PROJECT_SCRIPTS_H
#define CPP_PROJECT_SCRIPTS_H

#include <string>

class Scripts {

public:
    static void copyAndCompareCSV();
    static void codeAndDecodeCSV();
    static void codeCSV(std::string input_path, std::string input_filename, std::string output_path, std::string output_filename);
    static void decodeCSV(std::string input_path, std::string input_filename, std::string output_path, std::string output_filename);
};

#endif //CPP_PROJECT_SCRIPTS_H

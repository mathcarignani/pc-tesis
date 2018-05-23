
#ifndef CPP_PROJECT_SCRIPTS_H
#define CPP_PROJECT_SCRIPTS_H

#include <string>
#include "path.h"
#include <vector>

class Scripts {

public:
    static void codeBasic(Path input_path, Path output_path);
    static void decodeBasic(Path input_path, Path output_path);

    static void codePCA(Path input_path, Path output_path, int fixed_window_size, std::vector<int> error_thresholds_vector);
    static void decodePCA(Path input_path, Path output_path, int fixed_window_size);

    static void codeAPCA(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector);
    static void decodeAPCA(Path input_path, Path output_path, int max_window_size);


    static void copyAndCompareCSV();
    static void codeAndDecodeCSV();
    static void codeCSV(std::string input_path, std::string input_filename, std::string output_path, std::string output_filename);
    static void decodeCSV(std::string input_path, std::string input_filename, std::string output_path, std::string output_filename);
};

#endif //CPP_PROJECT_SCRIPTS_H

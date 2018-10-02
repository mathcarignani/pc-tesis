
#ifndef CPP_PROJECT_TESTS_CODERS_H
#define CPP_PROJECT_TESTS_CODERS_H

#include "iostream"
#include "dataset.h"
#include "csv_writer.h"

class TestsCoders {

public:
    static const std::string DATASETS_PATH;
    static const std::string TEST_OUTPUT_PATH;

    TestsCoders();
    void runAll();

    static void testSideFilderCoder();

private:
    std::vector<Path> paths;
    std::vector<std::vector<int>> lossless, lossy;
    std::string output_root_folder;
    CSVWriter* bits_csv;
    std::string coder_name;
    Path expected_code_path, output_code_path, output_decode_path;
    std::string expected_path_str, output_path_str;
    Path file_path;

    void setDatasets();
    void setCoderPaths(std::string coder_name_);
};

#endif //CPP_PROJECT_TESTS_CODERS_H

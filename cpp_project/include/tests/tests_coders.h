
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
    int win_size;
    Dataset ds;
    std::vector<int> errors_vector;
    std::string expected_root_folder;
    std::string output_root_folder;
    CSVWriter* bits_csv;
    std::string coder_name;
    Path expected_code_path, output_code_path, output_decode_path;
    std::string expected_path_str, output_path_str;
    Path file_path;
    std::string mode;

    void setDatasets();
    void setCoderPaths(std::string coder_name_);
    void setModePaths(int i);
    void testCoderBasic();
    void testCoderPCA();
    void testCoderAPCA();
    void testCoderPWLHInt();
    void testCoderPWLH();
    void testCoderCA();

};

#endif //CPP_PROJECT_TESTS_CODERS_H

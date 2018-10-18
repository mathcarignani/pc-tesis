
#ifndef CPP_PROJECT_TESTS_HEADER_CODER_H
#define CPP_PROJECT_TESTS_HEADER_CODER_H

#include "dataset.h"
#include "header_coder.h"

class TestsHeaderCoder {

public:
    TestsHeaderCoder();
    void runAll();

private:
    CSVReader* input_csv;
    BitStreamWriter* output_file;
    Path coded_file_path;
    Dataset* dataset;
    std::vector<ColumnCode*> column_code_vector;
    ColumnCode* column_code;

    void codeHeader(Path path);
    void checkColumnCode(int index, Range range, int bits, int offset, int nan);

    void testColumnCodeVector();
    void testUpdateRangesGAMPS();

};

#endif //CPP_PROJECT_TESTS_HEADER_CODER_H

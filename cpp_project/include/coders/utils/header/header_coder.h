
#ifndef CPP_PROJECT_HEADER_CODER_H
#define CPP_PROJECT_HEADER_CODER_H

#include <iostream>
#include "coder_common.h"
#include "csv_reader.h"
#include "dataset.h"
#include "dataset_utils.h"


class HeaderCoder {

public:
    HeaderCoder(CSVReader* input_csv_, BitStreamWriter* output_file_); // test_mode = true
    HeaderCoder(CSVReader* input_csv_, CoderCommon* coder_common_); // test_mode = false
    void codeHeader(Dataset* dataset);
    static const int HEADER_LINES; // number of lines used for the header in the .csv

private:
    CSVReader* input_csv;
    BitStreamWriter* output_file;
    CoderCommon* coder_common;
    bool test_mode;

    std::string codeDatasetName(DatasetUtils & dataset_utils);
    void codeTimeUnit(DatasetUtils & dataset_utils);
    void codeFirstTimestamp();
    static long int codeTimestamp(std::string timestamp_str);
    int codeColumnNames();
};

#endif //CPP_PROJECT_HEADER_CODER_H

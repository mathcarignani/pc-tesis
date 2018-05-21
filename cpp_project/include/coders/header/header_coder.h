
#ifndef CPP_PROJECT_HEADER_CODER_H
#define CPP_PROJECT_HEADER_CODER_H

#include <iostream>
#include "bit_stream_writer.h"
#include "csv_reader.h"
#include "dataset.h"
#include "dataset_utils.h"


class HeaderCoder {

public:
    HeaderCoder(CSVReader &input_csv, BitStreamWriter &output_file) : input_csv(input_csv), output_file(output_file) { }
    Dataset codeHeader();

private:
    CSVReader &input_csv;
    BitStreamWriter &output_file;
    std::string codeDatasetName(DatasetUtils & dataset_utils);
    void codeTimeUnit(DatasetUtils & dataset_utils);
    void codeFirstTimestamp();
    static long int codeTimestamp(std::string timestamp_str);
    int codeColumnNames();
};

#endif //CPP_PROJECT_HEADER_CODER_H

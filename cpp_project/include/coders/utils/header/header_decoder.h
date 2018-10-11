
#ifndef CPP_PROJECT_HEADER_DECODER_H
#define CPP_PROJECT_HEADER_DECODER_H

#include <iostream>
#include "bit_stream_reader.h"
#include "csv_writer.h"
#include "dataset.h"
#include "dataset_utils.h"


class HeaderDecoder {

public:
    HeaderDecoder(BitStreamReader* input_file_, CSVWriter* output_csv_);
    Dataset* decodeHeader();

private:
    BitStreamReader* input_file;
    CSVWriter* output_csv;
    std::string decodeDatasetName(DatasetUtils & dataset_utils);
    void decodeTimeUnit(DatasetUtils & dataset_utils);
    void decodeFirstTimestamp();
    static std::string decodeTimestamp(long int seconds);
    int decodeColumnNames();
};

#endif //CPP_PROJECT_HEADER_DECODER_H

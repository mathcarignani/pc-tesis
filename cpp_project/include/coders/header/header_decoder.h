
#ifndef CPP_PROJECT_HEADER_DECODER_H
#define CPP_PROJECT_HEADER_DECODER_H

#include <iostream>
#include "bit_stream_reader.h"
#include "csv_writer.h"
#include "dataset.h"
#include "dataset_utils.h"


class HeaderDecoder {

public:
    HeaderDecoder(BitStreamReader &input_file, CSVWriter &output_csv) : input_file(input_file), output_csv(output_csv) { }
    Dataset decodeHeader();

private:
    BitStreamReader &input_file;
    CSVWriter &output_csv;
    void decodeDatasetName(DatasetUtils & dataset_utils);
    void decodeTimeUnit(DatasetUtils & dataset_utils);
    void decodeFirstTimestamp();
    static std::string decodeTimestamp(long int seconds);
    void decodeColumnNames();
};

#endif //CPP_PROJECT_HEADER_DECODER_H

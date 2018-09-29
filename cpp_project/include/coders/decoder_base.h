
#ifndef CPP_PROJECT_DECODER_BASE_H
#define CPP_PROJECT_DECODER_BASE_H

#include "bit_stream_reader.h"
#include "csv_writer.h"
#include "dataset.h"
#include "constants.h"


class DecoderBase {

private:
    void decodeDataRowsCount();
    virtual void decodeDataRows() = 0;
    std::string decodeValue(int y);
    int decodeRaw();

protected:
    BitStreamReader* input_file;
    CSVWriter* output_csv;
    Dataset dataset;
    int data_columns_count;
    int data_rows_count;

    bool decodeBool();
    int decodeInt(int bits);
    std::string decodeValueRaw();
    float decodeFloat();

public:
    DecoderBase(BitStreamReader* input_file_, CSVWriter* output_csv_);
    void decodeFile();
    void close();
};

#endif //CPP_PROJECT_DECODER_BASE_H


#ifndef CPP_PROJECT_DECODER_BASE_H
#define CPP_PROJECT_DECODER_BASE_H

#include "bit_stream_reader.h"
#include "csv_writer.h"
#include "dataset.h"


class DecoderBase {

private:
    void decodeDataRowsCount();
    virtual void decodeDataRows() = 0;
    std::string decodeValue(int y);
    int decodeRaw();

protected:
    BitStreamReader &input_file;
    CSVWriter &output_csv;
    Dataset dataset;
    int data_columns_count;
    int data_rows_count;

    std::string decodeValueRaw();
    float decodeFloat();

public:
    std::string NO_DATA = "N";
    char NO_DATA_CHAR = 'N';
    DecoderBase(BitStreamReader &input_file, CSVWriter &output_csv) : input_file(input_file), output_csv(output_csv) { }
    void decodeFile();
    void close();
};

#endif //CPP_PROJECT_DECODER_BASE_H

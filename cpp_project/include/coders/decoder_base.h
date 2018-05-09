
#ifndef CPP_PROJECT_DECODER_BASE_H
#define CPP_PROJECT_DECODER_BASE_H

#include "bit_stream_reader.h"
#include "csv_writer.h"


class DecoderBase {

private:
    BitStreamReader &input_file;
    CSVWriter &output_csv;
    //    Dataset dataset;
    int data_columns_count;
    int data_rows_count;

    void decodeDataRowsCount();
    void decodeDataRows() = 0;
    void decodeValue(std::string y, int row_index, int col_index);
    void decodeRaw();
    void decodeValueRaw(int row_index, int col_index);

public:
    DecoderBase(BitStreamReader &input_file, CSVWriter &output_csv) : input_file(input_file), output_csv(output_csv) { }
    void decodeFile();
    void close();
};

#endif //CPP_PROJECT_DECODER_BASE_H

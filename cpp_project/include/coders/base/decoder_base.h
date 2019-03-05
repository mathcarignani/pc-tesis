
#ifndef CPP_PROJECT_DECODER_BASE_H
#define CPP_PROJECT_DECODER_BASE_H

#include "bit_stream_reader.h"
#include "csv_writer.h"
#include "dataset.h"
#include "constants.h"
#include "mask.h"

class DecoderBase {

private:
    void decodeDataRowsCount();
    virtual void decodeDataRows() = 0;
    std::string decodeValue(int y);
    int decodeRaw();

protected:
    CSVWriter* output_csv;
    Dataset* dataset;
    int window_size;

    void transposeMatrix(int data_rows_count_, std::vector<std::vector<std::string>> columns, int total_columns);

public:
    BitStreamReader* input_file;
    int data_rows_count;
    std::vector<int> time_delta_vector;
    int window_size_bit_length;
    int row_index;
#if MASK_MODE
    Mask* mask;
#endif

    static DecoderBase* getDecoder(BitStreamReader* input_file, CSVWriter* output_csv);

    DecoderBase(BitStreamReader* input_file_, CSVWriter* output_csv_);
    void decodeFile();
    void close();

    bool decodeBool();
    int decodeInt(int bits);
    int decodeUnary();
    std::string decodeValueRaw();

    float decodeFloat();
    double decodeDouble();
    int decodeInt();
    void completeByte();

    void setWindowSize(int window_size_);
};

#endif //CPP_PROJECT_DECODER_BASE_H

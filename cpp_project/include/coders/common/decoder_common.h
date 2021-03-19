
#ifndef CPP_PROJECT_DECODER_COMMON_H
#define CPP_PROJECT_DECODER_COMMON_H

#include "bit_stream_reader.h"
#include "csv_writer.h"
#include "dataset.h"
#include "constants.h"
#include "mask.h"

class DecoderCommon {

private:
    void decodeDataRowsCount();
    virtual void decodeDataRows() = 0;
    std::string decodeValue(int y);
    int decodeRaw();

    static std::string decodeCoderName(BitStreamReader* input_file);
    static int decodeWindowParameter(BitStreamReader* input_file);

protected:
    CSVWriter* output_csv;
    Dataset* dataset;
    int window_size;
    std::string coder_name;

    void transposeMatrix(int data_rows_count_, std::vector<std::vector<std::string>> columns, int total_columns);

public:
    BitStreamReader* input_file;
    int data_rows_count;
    std::vector<int> time_delta_vector;
    int window_size_bit_length;
    int row_index;
#if MASK_MODE
    Mask* mask;
#if MASK_MODE == 3
    std::vector<Mask*> masks_vector;
#endif // MASK_MODE == 3
#endif // MASK_MODE

    static DecoderCommon* getDecoder(BitStreamReader* input_file, CSVWriter* output_csv);

    DecoderCommon(std::string coder_name_, BitStreamReader* input_file_, CSVWriter* output_csv_);
    void decodeFile();
    void close();

    bool decodeBool();
    int decodeInt(int bits);
    int decodeWindowLength(int window_size_bit_length);
    int decodeWindowLength();
    int decodeUnary();
    std::string decodeValueRaw();

    float decodeFloat();
    void flushByte();

    void setWindowSize(int window_size_);
};

#endif //CPP_PROJECT_DECODER_COMMON_H


#ifndef CPP_PROJECT_DECODER_INPUT_H
#define CPP_PROJECT_DECODER_INPUT_H

#include "bit_stream_reader.h"

class DecoderInput {

private:
    BitStreamReader* input_file;
    bool print_;
    int bit_count;
    int byte_count;
    int byte_count_start;

public:
    DecoderInput(BitStreamReader* input_file_);
    int get_bit();
    void print();
    void setByteCount(int byte_count_);
};

#endif //CPP_PROJECT_DECODER_INPUT_H

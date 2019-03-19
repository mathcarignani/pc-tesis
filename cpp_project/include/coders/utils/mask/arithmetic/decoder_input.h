
#ifndef CPP_PROJECT_DECODER_INPUT_H
#define CPP_PROJECT_DECODER_INPUT_H

#include "bit_stream_reader.h"

class DecoderInput {

private:
    BitStreamReader* input_file;

public:
    DecoderInput(BitStreamReader* input_file_);
    int get_bit();
};

#endif //CPP_PROJECT_DECODER_INPUT_H

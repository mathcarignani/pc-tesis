
#ifndef CPP_PROJECT_DECODER_OUTPUT_H
#define CPP_PROJECT_DECODER_OUTPUT_H

#include "mask.h"

class DecoderOutput {

private:
    Mask* mask;
    Burst* burst;
    int row_index;

public:
    DecoderOutput(Mask* mask_);
    void putByte(int c);
    void close();
};

#endif //CPP_PROJECT_DECODER_OUTPUT_H

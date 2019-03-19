
#ifndef CPP_PROJECT_DECODER_OUTPUT_H
#define CPP_PROJECT_DECODER_OUTPUT_H

#include "mask.h"

class DecoderOutput {

private:
    Mask* mask;
    Burst* burst;
    int row_index;
    int data_rows_count;

public:
    DecoderOutput(Mask* mask_, int data_rows_count_);
    bool putByte(int c);
    void close();
};

#endif //CPP_PROJECT_DECODER_OUTPUT_H


#ifndef CPP_PROJECT_GOLOMB_DECODER_H
#define CPP_PROJECT_GOLOMB_DECODER_H

#include "decoder_base.h"

class GolombDecoder {

private:
    DecoderBase* decoder;
    bool no_data_majority;
    int l;
    int k;
    int decodeRunLength(Mask* mask, int remaining);
    int decodeLength();

public:
    GolombDecoder(DecoderBase* decoder_);
    void decode(Mask* mask);

};

#endif //CPP_PROJECT_GOLOMB_DECODER_H

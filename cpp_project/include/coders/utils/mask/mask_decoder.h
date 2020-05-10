
#ifndef CPP_PROJECT_MASK_DECODER_H
#define CPP_PROJECT_MASK_DECODER_H

#include "simple_mask_decoder.h"
#include "golomb_mask_decoder.h"
#include "arithmetic_mask_decoder.h"

#if MASK_MODE

class MaskDecoder {

public:
    static Mask* decode(DecoderCommon* decoder);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_MASK_DECODER_H

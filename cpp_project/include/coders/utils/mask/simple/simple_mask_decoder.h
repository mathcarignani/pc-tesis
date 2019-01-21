
#ifndef CPP_PROJECT_SIMPLE_MASK_DECODER_H
#define CPP_PROJECT_SIMPLE_MASK_DECODER_H

#include "constants.h"

#if MASK_MODE

#include "mask.h"
#include "decoder_base.h"

class SimpleMaskDecoder {

public:
    static Mask* decode(DecoderBase* decoder);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_SIMPLE_MASK_DECODER_H

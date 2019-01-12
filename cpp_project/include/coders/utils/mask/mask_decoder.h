
#ifndef CPP_PROJECT_MASK_DECODER_H
#define CPP_PROJECT_MASK_DECODER_H

#include "burst_mask_decoder.h"

#if MASK_MODE

class MaskDecoder {

public:
    static Mask* decode(DecoderBase* decoder);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_MASK_DECODER_H

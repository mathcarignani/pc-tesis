
#ifndef CPP_PROJECT_MASK_DECODER_H
#define CPP_PROJECT_MASK_DECODER_H

#include "burst_mask_decoder.h"

#if MASK_MODE

class MaskDecoder {

public:
    static Mask* decode(DecoderBase* decoder){
    #if BURST_MODE
        return BurstMaskDecoder::decode(decoder);
    #else
        // TODO
        // return GolombMaskDecoder::decode(decoder);
    #endif
    }

};

#endif // MASK_MODE

#endif //CPP_PROJECT_MASK_DECODER_H

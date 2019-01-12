
#include "mask_decoder.h"

#if MASK_MODE

Mask* MaskDecoder::decode(DecoderBase* decoder){
#if BURST_MODE
    return BurstMaskDecoder::decode(decoder);
#else
    // TODO
    // return GolombMaskDecoder::decode(decoder);
#endif // BURST_MODE
}

#endif // MASK_MODE

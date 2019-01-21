
#include "mask_decoder.h"

#if MASK_MODE

Mask* MaskDecoder::decode(DecoderBase* decoder){
#if GOLOMB_MODE
    return GolombMaskDecoder::decode(decoder);
#else
    return SimpleMaskDecoder::decode(decoder);
#endif // GOLOMB_MODE
}

#endif // MASK_MODE

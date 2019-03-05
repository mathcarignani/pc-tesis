
#include "mask_decoder.h"

#if MASK_MODE

Mask* MaskDecoder::decode(DecoderBase* decoder){
#if MASK_MODE == 1
    return SimpleMaskDecoder::decode(decoder);
#elif MASK_MODE == 2
    return GolombMaskDecoder::decode(decoder);
#elif MASK_MODE == 3
    return ArithmeticMaskDecoder::decode(decoder);
#endif
}

#endif // MASK_MODE

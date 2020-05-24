
#include "mask_decoder.h"

#if MASK_MODE

Mask* MaskDecoder::decode(DecoderCommon* decoder){
#if MASK_MODE == 1
    return SimpleMaskDecoder::decode(decoder);
#elif MASK_MODE == 2
    return GolombMaskDecoder::decode(decoder);
#endif
}

#endif // MASK_MODE

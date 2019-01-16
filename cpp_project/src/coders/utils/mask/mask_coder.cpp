
#include "mask_coder.h"

#if MASK_MODE

int MaskCoder::code(CoderBase* coder, int column_index){
#if BURST_MODE
    return BurstMaskCoder::code(coder, column_index);
#else
    return GolombMaskCoder::code(coder, column_index);
#endif // BURST_MODE
}

#endif // MASK_MODE

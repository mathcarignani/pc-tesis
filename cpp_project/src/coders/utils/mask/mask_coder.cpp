
#include "mask_coder.h"

#if MASK_MODE

int MaskCoder::code(CoderBase* coder, int column_index){
#if GOLOMB_MODE
    return GolombMaskCoder::code(coder, column_index);
#else
    return SimpleMaskCoder::code(coder, column_index);
#endif // GOLOMB_MODE
}

#endif // MASK_MODE

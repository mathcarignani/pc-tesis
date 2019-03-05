
#include "mask_coder.h"

#if MASK_MODE

int MaskCoder::code(CoderBase* coder, int column_index){
#if MASK_MODE == 1
    return SimpleMaskCoder::code(coder, column_index);
#elif MASK_MODE == 2
    return GolombMaskCoder::code(coder, column_index);
#elif MASK_MODE == 3
    return ArithmeticMaskCoder::code(coder, column_index);
#endif
}

#endif // MASK_MODE

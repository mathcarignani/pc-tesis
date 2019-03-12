
#ifndef CPP_PROJECT_ARITHMETIC_MASK_CODER_H
#define CPP_PROJECT_ARITHMETIC_MASK_CODER_H

#include "constants.h"

#if MASK_MODE == 3

#include "mask.h"
#include "coder_base.h"

class ArithmeticMaskCoder {

public:
    static int code(CoderBase* coder, int column_index);

};

#endif // MASK_MODE == 3

#endif //CPP_PROJECT_ARITHMETIC_MASK_CODER_H


#ifndef CPP_PROJECT_ARITHMETIC_MASK_CODER_H
#define CPP_PROJECT_ARITHMETIC_MASK_CODER_H

#include "constants.h"

#if MASK_MODE

#include "mask.h"
#include "coder_base.h"

class ArithmeticMaskCoder {

public:
    static int code(CoderBase* coder, int column_index);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_ARITHMETIC_MASK_CODER_H

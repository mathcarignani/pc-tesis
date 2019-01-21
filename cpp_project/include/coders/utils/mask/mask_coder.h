
#ifndef CPP_PROJECT_MASK_CODER_H
#define CPP_PROJECT_MASK_CODER_H

#include "simple_mask_coder.h"
#include "golomb_mask_coder.h"

#if MASK_MODE

class MaskCoder {

public:
    static int code(CoderBase* coder, int column_index);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_MASK_CODER_H

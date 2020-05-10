
#ifndef CPP_PROJECT_SIMPLE_MASK_CODER_H
#define CPP_PROJECT_SIMPLE_MASK_CODER_H

#include "constants.h"

#if MASK_MODE

#include "mask.h"
#include "coder_common.h"

class SimpleMaskCoder {

private:
    static int codeBurst(CoderCommon* coder, Burst* burst);

public:
    static int code(CoderCommon* coder, int column_index);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_SIMPLE_MASK_CODER_H

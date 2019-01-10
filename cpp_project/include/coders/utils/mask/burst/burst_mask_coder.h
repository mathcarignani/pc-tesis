
#ifndef CPP_PROJECT_BURST_MASK_CODER_H
#define CPP_PROJECT_BURST_MASK_CODER_H

#include "constants.h"

#if MASK_MODE

#include "mask.h"
#include "coder_base.h"

class BurstMaskCoder {

private:
    static int codeBurst(CoderBase* coder, Burst* burst);

public:
    static int code(CoderBase* coder, int column_index);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_BURST_MASK_CODER_H

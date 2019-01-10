
#ifndef CPP_PROJECT_MASK_CODER_H
#define CPP_PROJECT_MASK_CODER_H

#include "burst_mask_coder.h"

#if MASK_MODE

class MaskCoder {

public:
    static int code(CoderBase* coder, int column_index){
    #if BURST_MODE
        return BurstMaskCoder::code(coder, column_index);
    #else
        // TODO
        // return GolombMaskCoder::code(coder, column_index);
    #endif
    }

};

#endif // MASK_MODE

#endif //CPP_PROJECT_MASK_CODER_H

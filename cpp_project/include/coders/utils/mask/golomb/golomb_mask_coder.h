
#ifndef CPP_PROJECT_GOLOMB_MASK_CODER_H
#define CPP_PROJECT_GOLOMB_MASK_CODER_H

#include "constants.h"

#if MASK_MODE

#include "mask.h"
#include "coder_base.h"

class GolombMaskCoder {

private:
    static int countTotalDataRows(CoderBase* coder, int column_index);

public:
    static int code(CoderBase* coder, int column_index);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_GOLOMB_MASK_CODER_H


#ifndef CPP_PROJECT_MASK_CODER_H
#define CPP_PROJECT_MASK_CODER_H

#include "constants.h"

#if MASK_MODE

#include "dataset.h"
#include "csv_reader.h"
#include "coder_base.h"
#include "mask.h"

class MaskCoder {

public:
    static int code(CoderBase* coder, int column_index);

private:
    static int codeBurst(CoderBase* coder, Burst* burst);
};

#endif // MASK_MODE

#endif //CPP_PROJECT_MASK_CODER_H

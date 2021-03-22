
#ifndef CPP_PROJECT_OUTPUT_H
#define CPP_PROJECT_OUTPUT_H

#include "constants.h"

#if MASK_MODE
#include "coder_common.h"

class CoderOutput {

private:
    CoderCommon* coder;

public:
    CoderOutput(CoderCommon* coder_);
    void put_bit(bool bit);
    void finishCoding(bool bit);
};
#endif // MASK_MODE

#endif //CPP_PROJECT_OUTPUT_H

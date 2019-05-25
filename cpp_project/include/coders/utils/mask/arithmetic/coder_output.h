
#ifndef CPP_PROJECT_OUTPUT_H
#define CPP_PROJECT_OUTPUT_H

#include "constants.h"

#if MASK_MODE == 3
#include "coder_base.h"

class CoderOutput {

private:
    CoderBase* coder;

public:
    CoderOutput(CoderBase* coder_);
    void put_bit(bool bit);
    void finishCoding(bool bit);
};
#endif // MASK_MODE == 3

#endif //CPP_PROJECT_OUTPUT_H

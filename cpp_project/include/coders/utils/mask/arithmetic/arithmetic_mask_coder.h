
#ifndef CPP_PROJECT_ARITHMETIC_MASK_CODER_H
#define CPP_PROJECT_ARITHMETIC_MASK_CODER_H

#include "constants.h"

#if MASK_MODE == 3

#define EOS_LENGTH 16 // used to mark the end of the stream

#include "mask.h"
#include "coder_base.h"

class ArithmeticMaskCoder {

private:
    CoderBase* coder;
    int column_index;

    void flush();

public:
    ArithmeticMaskCoder(CoderBase* coder_, int column_index_);
    int code();

};

#endif // MASK_MODE == 3

#endif //CPP_PROJECT_ARITHMETIC_MASK_CODER_H

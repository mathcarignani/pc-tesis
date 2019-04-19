
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
    int data_columns_count;

    void flush();
    std::vector<int> callCompress();

public:
    ArithmeticMaskCoder(CoderBase* coder_, int data_columns_count_);
    std::vector<int> code();

};

#endif // MASK_MODE == 3

#endif //CPP_PROJECT_ARITHMETIC_MASK_CODER_H

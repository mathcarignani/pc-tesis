
#ifndef CPP_PROJECT_ARITHMETIC_MASK_CODER_H
#define CPP_PROJECT_ARITHMETIC_MASK_CODER_H

#include "constants.h"

#if MASK_MODE

#define EOS_LENGTH 16 // used to mark the end of the stream

#include "mask.h"
#include "coder_common.h"

class ArithmeticMaskCoder {

private:
    CoderCommon* coder;
    int first_column_index = 1; // index of the first masked column
    int last_column_index = 0; // index of the last masked column


    void flush();
    std::vector<int> callCompress();

public:
    ArithmeticMaskCoder(CoderCommon* coder_, int first_column_index_, int last_column_index_);
    std::vector<int> code();

};

#endif // MASK_MODE

#endif //CPP_PROJECT_ARITHMETIC_MASK_CODER_H

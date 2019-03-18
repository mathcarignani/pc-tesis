
#ifndef CPP_PROJECT_ARITHMETIC_MASK_CODER_H
#define CPP_PROJECT_ARITHMETIC_MASK_CODER_H

#include "constants.h"

#if MASK_MODE == 3

#include "mask.h"
#include "coder_base.h"

class ArithmeticMaskCoder {

private:
    CoderBase* coder;
    int column_index;

    void flush();
    int callCompress(Path path);
    int callDecompress(Path path);
    void copyBytes(Path path, int total_bytes);

public:
    ArithmeticMaskCoder(CoderBase* coder_, int column_index_);
    int code();

};

#endif // MASK_MODE == 3

#endif //CPP_PROJECT_ARITHMETIC_MASK_CODER_H


#ifndef CPP_PROJECT_COLUMN_CODE_H
#define CPP_PROJECT_COLUMN_CODE_H

#include <vector>
#include "range.h"

class ColumnCode {

public:
    Range range;
    int bits;
    int offset;
    int nan;
    int total_bits = 0;
    int total_mask_bits = 0;

    ColumnCode();
    ColumnCode(Range range_, int bits_);
    void addBits(int bits_, bool mask_mode);
};

#endif //CPP_PROJECT_COLUMN_CODE_H

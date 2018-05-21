
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

    ColumnCode();
    ColumnCode(Range range_, int bits_);
    void addBits(int bits_);
};

#endif //CPP_PROJECT_COLUMN_CODE_H

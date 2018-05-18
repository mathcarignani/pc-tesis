
#ifndef CPP_PROJECT_CODER_BASIC_H
#define CPP_PROJECT_CODER_BASIC_H

#include "coder_cols.h"

class CoderBasic: public CoderCols {

private:
    void codeColumn() override;

public:
    using CoderCols::CoderCols;
};

#endif //CPP_PROJECT_CODER_BASIC_H


#ifndef CPP_PROJECT_CODER_BASIC_H
#define CPP_PROJECT_CODER_BASIC_H

#include "coder_cols.h"

class CoderBasic: public CoderCols {

private:
    void codeCoderParams() override;

    void codeColumnBefore() override;
    void codeColumnWhile(int value) override;
    void codeColumnAfter() override;

public:
    using CoderCols::CoderCols;
};

#endif //CPP_PROJECT_CODER_BASIC_H


#ifndef CPP_PROJECT_OUTPUT_H
#define CPP_PROJECT_OUTPUT_H

#include "coder_base.h"

class CoderOutput {

private:
    CoderBase* coder;

public:
    CoderOutput(CoderBase* coder_);
    void put_bit(bool bit);
    void finishCoding(bool bit);
};

#endif //CPP_PROJECT_OUTPUT_H
